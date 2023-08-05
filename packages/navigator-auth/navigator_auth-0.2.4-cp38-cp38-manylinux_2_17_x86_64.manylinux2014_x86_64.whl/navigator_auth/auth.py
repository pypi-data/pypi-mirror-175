"""Navigator Auth.

Navigator Authentication/Authorization system.

AuthHandler is the Authentication/Authorization system for NAV,
Supporting:
 * multiple authentication backends
 * authorization exceptions via middlewares
 * Session Support (on top of navigator-session)
"""
from textwrap import dedent
import importlib
import inspect
from collections.abc import Iterable
from aiohttp import web
from aiohttp.abc import AbstractView
import aiohttp_cors
from navigator_session import (
    SessionHandler, SESSION_KEY
)
from .conf import (
    AUTHENTICATION_BACKENDS,
    AUTHORIZATION_BACKENDS,
    AUTHORIZATION_MIDDLEWARES,
    AUTH_USER_MODEL,
    default_dsn,
    logging
)
### Table Handlers:
from .handlers import ClientHandler, OrganizationHandler, PermissionHandler, UserHandler, UserSession
from .handlers.program import ProgramCatHandler, ProgramHandler, ProgramClientHandler
from .handlers.groups import GroupHandler, GroupPermissionHandler, UserGroupHandler
## Responses
from .responses import JSONResponse
from .storages.postgres import PostgresStorage
from .backends.base import auth_middleware
from .authorizations import authz_hosts, authz_allow_hosts
from .exceptions import (
    AuthException,
    UserNotFound,
    InvalidAuth,
    FailedAuth,
    Forbidden,
    ConfigError
)

class AuthHandler:
    """Authentication Backend for Navigator."""
    name: str = 'auth'
    app: web.Application = None
    _template: str = """
        <!doctype html>
            <head></head>
            <body>
                <p>{message}</p>
                <form action="/login" method="POST">
                  Login:
                  <input type="text" name="login">
                  Password:
                  <input type="password" name="password">
                  <input type="submit" value="Login">
                </form>
                <a href="/logout">Logout</a>
            </body>
    """
    def __init__(
            self,
            app_name: str = 'auth',
            **kwargs
        ) -> None:
        self.name: str = app_name
        self.backends: dict = {}
        self._session = None
        self._template = dedent(self._template)
        authz_backends = self.get_authorization_backends(
            AUTHORIZATION_BACKENDS
        )
        if 'scheme' in kwargs:
            self.auth_scheme = kwargs['scheme']
        else:
            self.auth_scheme = 'Bearer'
        # Get User Model:
        try:
            user_model = self.get_usermodel(AUTH_USER_MODEL)
        except Exception as ex:
            raise ConfigError(
                f"Error Getting Auth User Model: {ex}"
            ) from ex
        args = {
            "scheme": self.auth_scheme,
            "authorization_backends": authz_backends,
            "user_model": user_model,
            **kwargs,
        }
        # get the authentication backends (all of the list)
        self.backends = self.get_backends(**args)
        self._middlewares = self.get_authorization_middlewares(
            AUTHORIZATION_MIDDLEWARES
        )
        # TODO: Session Support with parametrization (other backends):
        self._session = SessionHandler(storage='redis')

    async def auth_startup(self, app):
        """
        Some Authentication backends need to call an Startup.
        """
        for name, backend in self.backends.items():
            try:
                await backend.on_startup(app)
            except Exception as err:
                logging.exception(
                    f"Error on Startup Auth Backend {name} init: {err.message}"
                )
                raise AuthException(
                    f"Error on Startup Auth Backend {name} init: {err.message}"
                ) from err

    async def on_cleanup(self, app):
        """
        Cleanup the processes
        """
        for name, backend in self.backends.items():
            try:
                await backend.on_cleanup(app)
            except Exception as err:
                print(err)
                logging.exception(
                    f"Error on Cleanup Auth Backend {name} init: {err.message}"
                )
                raise AuthException(
                    f"Error on Cleanup Auth Backend {name} init: {err.message}"
                ) from err

    def get_backends(self, **kwargs):
        backends = {}
        for backend in AUTHENTICATION_BACKENDS:
            try:
                parts = backend.split(".")
                bkname = parts[-1]
                classpath = ".".join(parts[:-1])
                module = importlib.import_module(classpath, package=bkname)
                obj = getattr(module, bkname)
                logging.debug(f'Auth: Loading Backend {bkname}')
                backends[bkname] = obj(**kwargs)
            except ImportError as ex:
                raise ConfigError(
                    f"Error loading Auth Backend {backend}: {ex}"
                ) from ex
        return backends

    def get_usermodel(self, model: str):
        try:
            parts = model.split(".")
            name = parts[-1]
            classpath = ".".join(parts[:-1])
            module = importlib.import_module(classpath, package=name)
            obj = getattr(module, name)
            return obj
        except ImportError as ex:
            raise ConfigError(
                f"Auth: Error loading Auth User Model {model}: {ex}"
            ) from ex

    def get_authorization_backends(self, backends: Iterable) -> tuple:
        b = []
        for backend in backends:
            # TODO: more automagic logic
            if backend == "hosts":
                b.append(authz_hosts())
            elif backend == "allow_hosts":
                b.append(authz_allow_hosts())
        return b

    def get_authorization_middlewares(self, backends: Iterable) -> tuple:
        b = tuple()
        for backend in backends:
            try:
                parts = backend.split(".")
                bkname = parts[-1]
                classpath = ".".join(parts[:-1])
                module = importlib.import_module(classpath, package=bkname)
                obj = getattr(module, bkname)
                b.append(obj)
            except ImportError as ex:
                raise Exception(
                    f"Error loading Authz Middleware {backend}: {ex}"
                ) from ex
        return b

    async def api_logout(self, request: web.Request) -> web.Response:
        """Logout.
        API-based Logout.
        """
        try:
            await self._session.storage.forgot(request)
            return web.json_response(
                {
                    "message": "Logout successful",
                    "state": 202
                },
                status=202
            )
        except Exception as err:
            print(err)
            raise web.HTTPUnauthorized(
                reason=f"Logout Error {err.message}"
            )

    async def api_login(self, request: web.Request) -> web.Response:
        """Login.

        API based login.
        """
        # first: getting header for an existing backend
        method = request.headers.get('X-Auth-Method')
        if method:
            try:
                backend = self.backends[method]
            except KeyError as ex:
                raise web.HTTPUnauthorized(
                    reason=f"Unacceptable Auth Method {method}",
                    content_type="application/json"
                ) from ex
            try:
                userdata = await backend.authenticate(request)
                if not userdata:
                    raise web.HTTPForbidden(
                        reason='User was not authenticated'
                    )
            except (Forbidden, FailedAuth) as err:
                raise web.HTTPForbidden(
                    reason=f"{err.message}"
                )
            except InvalidAuth as err:
                logging.exception(err)
                raise web.HTTPForbidden(
                    reason=f"{err.message}"
                )
            except UserNotFound as err:
                raise web.HTTPForbidden(
                    reason=f"User Doesn't exists: {err.message}"
                )
            except Exception as err:
                raise web.HTTPClientError(
                    reason=f"{err.message}"
                )
            return JSONResponse(userdata, status=200)
        else:
            # second: if no backend declared, will iterate over all backends
            userdata = None
            for _, backend in self.backends.items():
                try:
                    # check credentials for all backends
                    userdata = await backend.authenticate(request)
                    if userdata:
                        break
                except (
                    AuthException,
                    UserNotFound,
                    InvalidAuth,
                    FailedAuth
                ) as err:
                    continue
                except Exception as err:
                    raise web.HTTPClientError(
                        reason=err
                    ) from err
            # if not userdata, then raise an not Authorized
            if not userdata:
                raise web.HTTPForbidden(
                    reason="Login Failure in all Auth Methods."
                )
            else:
                # at now: create the user-session
                try:
                    await self._session.storage.new_session(request, userdata)
                except Exception as err:
                    raise web.HTTPUnauthorized(
                        reason=f"Error Creating User Session: {err.message}"
                    ) from err
                return JSONResponse(userdata, status=200)

    # Session Methods:
    async def forgot_session(self, request: web.Request):
        await self._session.storage.forgot(request)

    async def create_session(self, request: web.Request, data: Iterable):
        return await self._session.storage.new_session(request, data)

    async def get_session(self, request: web.Request) -> web.Response:
        """ Get user data from session."""
        session = None
        try:
            session = await self._session.storage.get_session(request)
        except AuthException as err:
            response = {
                "message": "Session Error",
                "error": err.message,
                "status": err.state,
            }
            return JSONResponse(response, status=err.state)
        except Exception as err:
            raise web.HTTPClientError(
                reason=err
            ) from err
        if not session:
            try:
                session = await self._session.storage.get_session(request)
            except Exception: # pylint: disable=W0703
                # always return a null session for user:
                session = await self._session.storage.new_session(request, {})
        userdata = dict(session)
        try:
            del userdata['user']
        except KeyError:
            pass
        return JSONResponse(userdata, status=200)


    async def get_auth(
        self,
        request: web.Request
    ) -> str:
        """
        Get the current User ID from Request
        """
        return request.get(SESSION_KEY, None)

    async def get_userdata(
        self,
        request: web.Request
    ) -> str:
        """
        Get the current User ID from Request
        """
        data = request.get(self.user_property, None)
        if data:
            return data
        else:
            raise web.HTTPForbidden(
                reason="Auth: User Data is missing on Request."
            )

    def setup_cors(self, cors):
        for route in list(self.app.router.routes()):
            try:
                if inspect.isclass(route.handler) and issubclass(
                    route.handler, AbstractView
                ):
                    cors.add(route, webview=True)
                else:
                    cors.add(route)
            except (TypeError, ValueError):
                pass

    def setup(self, app: web.Application) -> web.Application:
        if isinstance(app, web.Application):
            self.app = app # register the app into the Extension
        else:
            self.app = app.get_app() # Nav Application
        ## Manager for Auth Storage and Policy Storage
        ## getting Database Connection:
        try:
            pool = PostgresStorage(driver='pg', dsn=default_dsn)
            pool.configure(self.app) # pylint: disable=E1123
        except RuntimeError as ex:
            raise web.HTTPServerError(
                reason=f"Error creating Database connection: {ex}"
            )
        # startup operations over extension backend
        self.app.on_startup.append(
            self.auth_startup
        )
        # cleanup operations over Auth backend
        self.app.on_cleanup.append(
            self.on_cleanup
        )
        logging.debug(':::: Auth Handler Loaded ::::')
        ## also, load the Session System
        # configuring Session Object
        self._session.setup(self.app)
        # register the Auth extension into the app
        self.app[self.name] = self
        ## Configure Routes
        router = self.app.router
        router.add_route(
            "GET",
            "/api/v1/login",
            self.api_login,
            name="api_login"
        )
        router.add_route(
            "POST",
            "/api/v1/login",
            self.api_login,
            name="api_login_post"
        )
        router.add_route(
            "GET",
            "/api/v1/logout",
            self.api_logout,
            name="api_logout"
        )
        # get the session information for a program (only)
        router.add_route(
            "GET",
            "/api/v1/session/{program}",
            self.get_session,
            name="api_session_tenant",
        )
        # get all user information
        router.add_route(
            "GET",
            "/api/v1/user/session",
            self.get_session,
            name="api_session"
        )
        ### Handler for Auth Objects:
        self.model_routes(router)
        # the backend add a middleware to the app
        mdl = self.app.middlewares
        # first: add the basic jwt middleware (used by basic auth and others)
        mdl.append(auth_middleware)
        # if authentication backend needs initialization
        for name, backend in self.backends.items():
            try:
                # backend.configure(app, router, handler=app)
                backend.configure(self.app, router)
                if hasattr(backend, "auth_middleware"):
                    # add the middleware for this backend Authentication
                    mdl.append(backend.auth_middleware)
            except Exception as err:
                logging.exception(
                    f"Auth: Error on Backend {name} init: {err!s}"
                )
                raise ConfigError(
                    f"Auth: Error on Backend {name} init: {err!s}"
                ) from err
        # at the End: configure CORS for routes:
        cors = aiohttp_cors.setup(
            self.app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_methods="*",
                    allow_headers="*",
                    max_age=3600,
                )
            },
        )
        self.setup_cors(cors)
        return self.app

    def model_routes(self, router):
        ## Clients
        router.add_view(
            r'/api/v1/clients/{id:.*}',
            ClientHandler,
            name='api_clients_id'
        )
        router.add_view(
            r'/api/v1/clients{meta:\:?.*}',
            ClientHandler,
            name='api_clients'
        )
        ## Organizations:
        router.add_view(
            r'/api/v1/organizations/{id:.*}',
            OrganizationHandler,
            name='api_organizations_id'
        )
        router.add_view(
            r'/api/v1/organizations{meta:\:?.*}',
            OrganizationHandler,
            name='api_organizations'
        )
        ### Programs:
        router.add_view(
            r'/api/v1/programs/{id:.*}',
            ProgramHandler,
            name='api_programs_id'
        )
        router.add_view(
            r'/api/v1/programs{meta:\:?.*}',
            ProgramHandler,
            name='api_programs'
        )
        router.add_view(
            r'/api/v1/program_categories/{id:.*}',
            ProgramCatHandler,
            name='api_program_categories_id'
        )
        router.add_view(
            r'/api/v1/program_categories{meta:\:?.*}',
            ProgramCatHandler,
            name='api_program_categories'
        )
        # Program Client:
        router.add_view(
            r'/api/v1/program_clients/{id:.*}',
            ProgramClientHandler,
            name='api_programs_clients_id'
        )
        router.add_view(
            r'/api/v1/program_clients{meta:\:?.*}',
            ProgramClientHandler,
            name='api_programs_clients'
        )
        ### Model permissions:
        router.add_view(
            r'/api/v1/permissions/{id:.*}',
            PermissionHandler,
            name='api_permissions_id'
        )
        router.add_view(
            r'/api/v1/permissions{meta:\:?.*}',
            PermissionHandler,
            name='api_permissions'
        )
        ### Groups:
        router.add_view(
            r'/api/v1/groups/{id:.*}',
            GroupHandler,
            name='api_groups_id'
        )
        router.add_view(
            r'/api/v1/groups{meta:\:?.*}',
            GroupHandler,
            name='api_groups'
        )
        router.add_view(
            r'/api/v1/user_groups/{id:.*}',
            UserGroupHandler,
            name='api_user_groups_id'
        )
        router.add_view(
            r'/api/v1/user_groups{meta:\:?.*}',
            UserGroupHandler,
            name='api_user_groups'
        )
        router.add_view(
            r'/api/v1/group_permissions/{id:.*}',
            GroupPermissionHandler,
            name='api_group_permissions_id'
        )
        router.add_view(
            r'/api/v1/group_permissions{meta:\:?.*}',
            GroupPermissionHandler,
            name='api_group_permissions'
        )
        ### User Methods:
        router.add_view(
            r'/api/v1/users/{id:.*}',
            UserHandler,
            name='api_auth_users_id'
        )
        router.add_view(
            r'/api/v1/users{meta:\:?.*}',
            UserHandler,
            name='api_auth_users'
        )
        ### User Session Methods:
        usr = UserSession()
        router.add_get("/api/v2/user/logout", usr.logout, allow_head=True)
        router.add_delete("/api/v2/user/logout", usr.logout)
        router.add_get("/api/v2/user/session", usr.user_session, allow_head=True)
        router.add_get("/api/v2/user/profile", usr.user_profile, allow_head=True)
        router.add_put("/api/v2/user/in_session", usr.in_session)
        router.add_post("/api/v2/user/set_password", usr.password_change)
        router.add_post("/api/v2/user/password_reset/{userid:.*}", usr.password_reset)
        router.add_get("/api/v2/user/gen_token/{userid:.*}", usr.gen_token, allow_head=True)
