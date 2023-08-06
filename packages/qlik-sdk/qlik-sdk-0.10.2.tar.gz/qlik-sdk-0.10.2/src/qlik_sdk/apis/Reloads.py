# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services 0.478.8

from __future__ import annotations

from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Reload:
    """

    Attributes
    ----------
    appId: str
      The ID of the app.
    creationTime: str
      The time the reload job was created.
    endTime: str
      The time the reload job finished.
    engineTime: str
      The timestamp returned from the Sense engine upon successful reload.
    id: str
      The ID of the reload.
    links: ReloadLinks
    log: str
      The log describing the result of the reload request.
    partial: bool
      The boolean value used to present the reload is partial or not
    startTime: str
      The time the reload job was consumed from the queue.
    status: str
      The status of the reload. There are seven statuses. `QUEUED`, `RELOADING`, `CANCELING` are the active statuses. `SUCCEEDED`, `FAILED`,`CANCELED`,`EXCEEDED_LIMIT` are the end statuses.
    tenantId: str
      The ID of the tenant who owns the reload.
    type: str
      The type of reload event (hub, chronos or external).
    userId: str
      The ID of the user who created the reload.
    """

    appId: str = None
    creationTime: str = None
    endTime: str = None
    engineTime: str = None
    id: str = None
    links: ReloadLinks = None
    log: str = None
    partial: bool = None
    startTime: str = None
    status: str = None
    tenantId: str = None
    type: str = None
    userId: str = None

    def __init__(self_, **kvargs):

        if "appId" in kvargs:
            if type(kvargs["appId"]).__name__ == self_.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "creationTime" in kvargs:
            if (
                type(kvargs["creationTime"]).__name__
                == self_.__annotations__["creationTime"]
            ):
                self_.creationTime = kvargs["creationTime"]
            else:
                self_.creationTime = kvargs["creationTime"]
        if "endTime" in kvargs:
            if type(kvargs["endTime"]).__name__ == self_.__annotations__["endTime"]:
                self_.endTime = kvargs["endTime"]
            else:
                self_.endTime = kvargs["endTime"]
        if "engineTime" in kvargs:
            if (
                type(kvargs["engineTime"]).__name__
                == self_.__annotations__["engineTime"]
            ):
                self_.engineTime = kvargs["engineTime"]
            else:
                self_.engineTime = kvargs["engineTime"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ == self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ReloadLinks(**kvargs["links"])
        if "log" in kvargs:
            if type(kvargs["log"]).__name__ == self_.__annotations__["log"]:
                self_.log = kvargs["log"]
            else:
                self_.log = kvargs["log"]
        if "partial" in kvargs:
            if type(kvargs["partial"]).__name__ == self_.__annotations__["partial"]:
                self_.partial = kvargs["partial"]
            else:
                self_.partial = kvargs["partial"]
        if "startTime" in kvargs:
            if type(kvargs["startTime"]).__name__ == self_.__annotations__["startTime"]:
                self_.startTime = kvargs["startTime"]
            else:
                self_.startTime = kvargs["startTime"]
        if "status" in kvargs:
            if type(kvargs["status"]).__name__ == self_.__annotations__["status"]:
                self_.status = kvargs["status"]
            else:
                self_.status = kvargs["status"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ == self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "userId" in kvargs:
            if type(kvargs["userId"]).__name__ == self_.__annotations__["userId"]:
                self_.userId = kvargs["userId"]
            else:
                self_.userId = kvargs["userId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def cancel(self) -> None:
        """
        Cancels a reload
        Cancels a reload that is in progress or has been queued

        Parameters
        ----------
        """
        self.auth.rest(
            path="/reloads/{reloadId}/actions/cancel".replace("{reloadId}", self.id),
            method="POST",
            params={},
            data=None,
        )


@dataclass
class ReloadLinks:
    """

    Attributes
    ----------
    self: ReloadsHref
    """

    self: ReloadsHref = None

    def __init__(self_, **kvargs):

        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = ReloadsHref(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ReloadRequest:
    """

    Attributes
    ----------
    appId: str
      The ID of the app to be reloaded.
    partial: bool
      The boolean value used to present the reload is partial or not
    """

    appId: str = None
    partial: bool = None

    def __init__(self_, **kvargs):

        if "appId" in kvargs:
            if type(kvargs["appId"]).__name__ == self_.__annotations__["appId"]:
                self_.appId = kvargs["appId"]
            else:
                self_.appId = kvargs["appId"]
        if "partial" in kvargs:
            if type(kvargs["partial"]).__name__ == self_.__annotations__["partial"]:
                self_.partial = kvargs["partial"]
            else:
                self_.partial = kvargs["partial"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ReloadsClass:
    """

    Attributes
    ----------
    data: list[Reload]
    links: ReloadsLinks
    """

    data: list[Reload] = None
    links: ReloadsLinks = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Reload(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ReloadsLinks(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ReloadsLinks:
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ReloadsHref:
    """

    Attributes
    ----------
    href: str
    """

    href: str = None

    def __init__(self_, **kvargs):

        if "href" in kvargs:
            if type(kvargs["href"]).__name__ == self_.__annotations__["href"]:
                self_.href = kvargs["href"]
            else:
                self_.href = kvargs["href"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Reloads:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get(self, reloadId: str) -> Reload:
        """
        Get reload record
        Finds and returns a reload record

        Parameters
        ----------
        reloadId: str
          The unique identifier of the reload.
        """
        response = self.auth.rest(
            path="/reloads/{reloadId}".replace("{reloadId}", reloadId),
            method="GET",
            params={},
            data=None,
        )
        obj = Reload(**response.json())
        obj.auth = self.auth
        return obj

    def get_reloads(
        self,
        appId: str,
        limit: int = 10,
        next: str = None,
        partial: bool = None,
        prev: str = None,
        max_items: int = 10,
    ) -> ListableResource[Reload]:
        """
        Finds and returns the reloads that the user has access to.

        Parameters
        ----------
        appId: str
          The UUID formatted string used to search for an app's reload history entries. TenantAdmin users may omit this parameter to list all reload history in the tenant.
        limit: int = 10
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        next: str = None
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.
        partial: bool = None
          The boolean value used to search for a reload is partial or not.
        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        """
        query_params = {}
        if appId is not None:
            query_params["appId"] = appId
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if partial is not None:
            query_params["partial"] = partial
        if prev is not None:
            query_params["prev"] = prev
        response = self.auth.rest(
            path="/reloads",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Reload,
            auth=self.auth,
            path="/reloads",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, data: ReloadRequest) -> Reload:
        """
        Reloads an app specified by an app ID.

        Parameters
        ----------
        data: ReloadRequest
          Request body specifying ID of app to be reloaded.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/reloads",
            method="POST",
            params={},
            data=data,
        )
        obj = Reload(**response.json())
        obj.auth = self.auth
        return obj
