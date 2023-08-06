# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services 0.478.8

from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class Space:
    """
    A space is a security context simplifying the management of access control by allowing users to control it on the containers instead of on the resources themselves.

    Attributes
    ----------
    createdAt: str
      The date and time when the space was created.
    createdBy: str
      The ID of the user who created the space.
    description: str
      The description of the space. Personal spaces do not have a description.
    id: str
      A unique identifier for the space, for example, 62716f4b39b865ece543cd45.
    links: SpaceLinks
    meta: SpaceMeta
      Information about the space settings.
    name: str
      The name of the space. Personal spaces do not have a name.
    ownerId: str
      The ID for the space owner.
    tenantId: str
      The ID for the tenant, for example, xqGQ0k66vSR8f9G7J-vYtHZQkiYrCpct.
    type: str
      The type of space such as shared, managed, and so on.
    updatedAt: str
      The date and time when the space was updated.
    """

    createdAt: str = None
    createdBy: str = None
    description: str = None
    id: str = None
    links: SpaceLinks = None
    meta: SpaceMeta = None
    name: str = None
    ownerId: str = None
    tenantId: str = None
    type: str = None
    updatedAt: str = None

    def __init__(self_, **kvargs):

        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ == self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs:
            if type(kvargs["createdBy"]).__name__ == self_.__annotations__["createdBy"]:
                self_.createdBy = kvargs["createdBy"]
            else:
                self_.createdBy = kvargs["createdBy"]
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                == self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ == self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = SpaceLinks(**kvargs["links"])
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ == self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = SpaceMeta(**kvargs["meta"])
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ == self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ == self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
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
        if "updatedAt" in kvargs:
            if type(kvargs["updatedAt"]).__name__ == self_.__annotations__["updatedAt"]:
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_assignments(
        self, limit: int = 10, next: str = None, prev: str = None, max_items: int = 10
    ) -> ListableResource[Assignment]:
        """
        Retrieves the assignments of the space matching the query.

        Parameters
        ----------
        limit: int = 10
          Maximum number of assignments to return.
        next: str = None
          The next page cursor. Next links make use of this.
        prev: str = None
          The previous page cursor. Previous links make use of this.
        """
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Assignment,
            auth=self.auth,
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            max_items=max_items,
            query_params=query_params,
        )

    def create_assignment(self, data: AssignmentCreate) -> Assignment:
        """
        Creates an assignment.

        Parameters
        ----------
        data: AssignmentCreate
          Attributes that the user wants to set for the assignment for the space.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            method="POST",
            params={},
            data=data,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj

    def create_shares_bulk(self, data: SharesCreate) -> SharesCreated:
        """
        Experimental
        Creates multiple shares.

        Parameters
        ----------
        data: SharesCreate

        """
        warnings.warn("create_shares_bulk is experimental", UserWarning, stacklevel=2)
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/{spaceId}/shares/bulk".replace("{spaceId}", self.id),
            method="POST",
            params={},
            data=data,
        )
        obj = SharesCreated(**response.json())
        obj.auth = self.auth
        return obj

    def get_shares(
        self,
        groupId: str = None,
        limit: int = 10,
        name: str = None,
        next: str = None,
        prev: str = None,
        resourceId: str = None,
        resourceType: str = None,
        userId: str = None,
        max_items: int = 10,
    ) -> ListableResource[Share]:
        """
        Experimental
        Retrieves the shares of the space matching the query.

        Parameters
        ----------
        groupId: str = None
          The groupId of the shared resource.
        limit: int = 10
          Maximum number of shares to return.
        name: str = None
          The name of the shared resource.
        next: str = None
          The next page cursor. Next links make use of this.
        prev: str = None
          The previous page cursor. Previous links make use of this.
        resourceId: str = None
          The ID of the shared resource.
        resourceType: str = None
          The type of the shared resource.
        userId: str = None
          The userId of the shared resource.
        """
        warnings.warn("get_shares is experimental", UserWarning, stacklevel=2)
        query_params = {}
        if groupId is not None:
            query_params["groupId"] = groupId
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if resourceId is not None:
            query_params["resourceId"] = resourceId
        if resourceType is not None:
            query_params["resourceType"] = resourceType
        if userId is not None:
            query_params["userId"] = userId
        response = self.auth.rest(
            path="/spaces/{spaceId}/shares".replace("{spaceId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Share,
            auth=self.auth,
            path="/spaces/{spaceId}/shares".replace("{spaceId}", self.id),
            max_items=max_items,
            query_params=query_params,
        )

    def create_share(self, data: ShareCreate) -> Share:
        """
        Experimental
        Creates a share.

        Parameters
        ----------
        data: ShareCreate

        """
        warnings.warn("create_share is experimental", UserWarning, stacklevel=2)
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/{spaceId}/shares".replace("{spaceId}", self.id),
            method="POST",
            params={},
            data=data,
        )
        obj = Share(**response.json())
        obj.auth = self.auth
        return obj

    def delete(self) -> None:
        """
        Deletes a space.

        Parameters
        ----------
        """
        self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(self, data: SpacePatch) -> Space:
        """
        Experimental
        Patches (updates) a space (partially).

        Parameters
        ----------
        data: SpacePatch
          Attribute that the user wants to patch (update) for the specified space.
        """
        warnings.warn("patch is experimental", UserWarning, stacklevel=2)
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="PATCH",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def set(self, data: SpaceUpdate) -> Space:
        """
        Experimental
        Updates a space.

        Parameters
        ----------
        data: SpaceUpdate
          Attributes that the user wants to update for the specified space.
        """
        warnings.warn("set is experimental", UserWarning, stacklevel=2)
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self


@dataclass
class Assignment:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    createdAt: str
      The date and time when the space was created.
    createdBy: str
      The ID of the user who created the assignment.
    id: str
    links: AssignmentLinks
    roles: list[str]
      The roles assigned to a user or group. Must not be empty.
    spaceId: str
      The unique identifier for the space.
    tenantId: str
      The unique identifier for the tenant.
    type: str
    updatedAt: str
      The date and time when the space was updated.
    updatedBy: str
      The ID of the user who updated the assignment.
    """

    assigneeId: str = None
    createdAt: str = None
    createdBy: str = None
    id: str = None
    links: AssignmentLinks = None
    roles: list[str] = None
    spaceId: str = None
    tenantId: str = None
    type: str = None
    updatedAt: str = None
    updatedBy: str = None

    def __init__(self_, **kvargs):

        if "assigneeId" in kvargs:
            if (
                type(kvargs["assigneeId"]).__name__
                == self_.__annotations__["assigneeId"]
            ):
                self_.assigneeId = kvargs["assigneeId"]
            else:
                self_.assigneeId = kvargs["assigneeId"]
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ == self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs:
            if type(kvargs["createdBy"]).__name__ == self_.__annotations__["createdBy"]:
                self_.createdBy = kvargs["createdBy"]
            else:
                self_.createdBy = kvargs["createdBy"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ == self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = AssignmentLinks(**kvargs["links"])
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ == self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ == self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
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
        if "updatedAt" in kvargs:
            if type(kvargs["updatedAt"]).__name__ == self_.__annotations__["updatedAt"]:
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]
        if "updatedBy" in kvargs:
            if type(kvargs["updatedBy"]).__name__ == self_.__annotations__["updatedBy"]:
                self_.updatedBy = kvargs["updatedBy"]
            else:
                self_.updatedBy = kvargs["updatedBy"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentCreate:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    roles: list[str]
      The roles assigned to the assigneeId.
    type: str
      The type of space such as shared, managed, and so on.
    """

    assigneeId: str = None
    roles: list[str] = None
    type: str = None

    def __init__(self_, **kvargs):

        if "assigneeId" in kvargs:
            if (
                type(kvargs["assigneeId"]).__name__
                == self_.__annotations__["assigneeId"]
            ):
                self_.assigneeId = kvargs["assigneeId"]
            else:
                self_.assigneeId = kvargs["assigneeId"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ == self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentLinks:
    """

    Attributes
    ----------
    self: SpacesLink
    space: SpacesLink
    """

    self: SpacesLink = None
    space: SpacesLink = None

    def __init__(self_, **kvargs):

        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = SpacesLink(**kvargs["self"])
        if "space" in kvargs:
            if type(kvargs["space"]).__name__ == self_.__annotations__["space"]:
                self_.space = kvargs["space"]
            else:
                self_.space = SpacesLink(**kvargs["space"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentUpdate:
    """

    Attributes
    ----------
    roles: list[str]
      The roles assigned to the assigneeId.
    """

    roles: list[str] = None

    def __init__(self_, **kvargs):

        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ == self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Assignments:
    """

    Attributes
    ----------
    data: list[Assignment]
    links: AssignmentsLinks
    meta: AssignmentsMeta
    """

    data: list[Assignment] = None
    links: AssignmentsLinks = None
    meta: AssignmentsMeta = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Assignment(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = AssignmentsLinks(**kvargs["links"])
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ == self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = AssignmentsMeta(**kvargs["meta"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsLinks:
    """

    Attributes
    ----------
    next: SpacesLink
    prev: SpacesLink
    self: SpacesLink
    """

    next: SpacesLink = None
    prev: SpacesLink = None
    self: SpacesLink = None

    def __init__(self_, **kvargs):

        if "next" in kvargs:
            if type(kvargs["next"]).__name__ == self_.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = SpacesLink(**kvargs["next"])
        if "prev" in kvargs:
            if type(kvargs["prev"]).__name__ == self_.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = SpacesLink(**kvargs["prev"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = SpacesLink(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class AssignmentsMeta:
    """

    Attributes
    ----------
    count: int
      The total number of assignments matching the current filter.
    """

    count: int = None

    def __init__(self_, **kvargs):

        if "count" in kvargs:
            if type(kvargs["count"]).__name__ == self_.__annotations__["count"]:
                self_.count = kvargs["count"]
            else:
                self_.count = kvargs["count"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FilterSpaces:
    """

    Attributes
    ----------
    ids: list[str]
    names: list[str]
    """

    ids: list[str] = None
    names: list[str] = None

    def __init__(self_, **kvargs):

        if "ids" in kvargs:
            if type(kvargs["ids"]).__name__ == self_.__annotations__["ids"]:
                self_.ids = kvargs["ids"]
            else:
                self_.ids = kvargs["ids"]
        if "names" in kvargs:
            if type(kvargs["names"]).__name__ == self_.__annotations__["names"]:
                self_.names = kvargs["names"]
            else:
                self_.names = kvargs["names"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class FineGrainedLicense:
    """

    Attributes
    ----------
    fineGrainedAppEnabled: bool
    """

    fineGrainedAppEnabled: bool = None

    def __init__(self_, **kvargs):

        if "fineGrainedAppEnabled" in kvargs:
            if (
                type(kvargs["fineGrainedAppEnabled"]).__name__
                == self_.__annotations__["fineGrainedAppEnabled"]
            ):
                self_.fineGrainedAppEnabled = kvargs["fineGrainedAppEnabled"]
            else:
                self_.fineGrainedAppEnabled = kvargs["fineGrainedAppEnabled"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Share:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    createdAt: str
    createdBy: str
      The ID of the user who created the share.
    id: str
    links: ShareLinks
    resourceId: str
      The ID of the shared resource.
    resourceName: str
      The name of the shared resource.
    resourceType: str
      The type of the shared resource.
    roles: list[ShareRoleType]
      The roles assigned to the assigneeId.
    spaceId: str
    tenantId: str
    type: str
    updatedAt: str
    updatedBy: str
      The ID of the user who updated the share.
    """

    assigneeId: str = None
    createdAt: str = None
    createdBy: str = None
    id: str = None
    links: ShareLinks = None
    resourceId: str = None
    resourceName: str = None
    resourceType: str = None
    roles: list[ShareRoleType] = None
    spaceId: str = None
    tenantId: str = None
    type: str = None
    updatedAt: str = None
    updatedBy: str = None

    def __init__(self_, **kvargs):

        if "assigneeId" in kvargs:
            if (
                type(kvargs["assigneeId"]).__name__
                == self_.__annotations__["assigneeId"]
            ):
                self_.assigneeId = kvargs["assigneeId"]
            else:
                self_.assigneeId = kvargs["assigneeId"]
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ == self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs:
            if type(kvargs["createdBy"]).__name__ == self_.__annotations__["createdBy"]:
                self_.createdBy = kvargs["createdBy"]
            else:
                self_.createdBy = kvargs["createdBy"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ == self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ShareLinks(**kvargs["links"])
        if "resourceId" in kvargs:
            if (
                type(kvargs["resourceId"]).__name__
                == self_.__annotations__["resourceId"]
            ):
                self_.resourceId = kvargs["resourceId"]
            else:
                self_.resourceId = kvargs["resourceId"]
        if "resourceName" in kvargs:
            if (
                type(kvargs["resourceName"]).__name__
                == self_.__annotations__["resourceName"]
            ):
                self_.resourceName = kvargs["resourceName"]
            else:
                self_.resourceName = kvargs["resourceName"]
        if "resourceType" in kvargs:
            if (
                type(kvargs["resourceType"]).__name__
                == self_.__annotations__["resourceType"]
            ):
                self_.resourceType = kvargs["resourceType"]
            else:
                self_.resourceType = kvargs["resourceType"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ == self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = [ShareRoleType(**e) for e in kvargs["roles"]]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ == self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
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
        if "updatedAt" in kvargs:
            if type(kvargs["updatedAt"]).__name__ == self_.__annotations__["updatedAt"]:
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]
        if "updatedBy" in kvargs:
            if type(kvargs["updatedBy"]).__name__ == self_.__annotations__["updatedBy"]:
                self_.updatedBy = kvargs["updatedBy"]
            else:
                self_.updatedBy = kvargs["updatedBy"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ShareCreate:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    resourceId: str
      The resource id for the shared item.
    resourceType: str
      The resource type for the shared item.
    roles: list[ShareRoleType]
      The roles assigned to the assigneeId.
    type: str
    """

    assigneeId: str = None
    resourceId: str = None
    resourceType: str = None
    roles: list[ShareRoleType] = None
    type: str = None

    def __init__(self_, **kvargs):

        if "assigneeId" in kvargs:
            if (
                type(kvargs["assigneeId"]).__name__
                == self_.__annotations__["assigneeId"]
            ):
                self_.assigneeId = kvargs["assigneeId"]
            else:
                self_.assigneeId = kvargs["assigneeId"]
        if "resourceId" in kvargs:
            if (
                type(kvargs["resourceId"]).__name__
                == self_.__annotations__["resourceId"]
            ):
                self_.resourceId = kvargs["resourceId"]
            else:
                self_.resourceId = kvargs["resourceId"]
        if "resourceType" in kvargs:
            if (
                type(kvargs["resourceType"]).__name__
                == self_.__annotations__["resourceType"]
            ):
                self_.resourceType = kvargs["resourceType"]
            else:
                self_.resourceType = kvargs["resourceType"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ == self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = [ShareRoleType(**e) for e in kvargs["roles"]]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ShareCreated:
    """

    Attributes
    ----------
    error: SpacesError
      An error object.
    share: Share
    """

    error: SpacesError = None
    share: Share = None

    def __init__(self_, **kvargs):

        if "error" in kvargs:
            if type(kvargs["error"]).__name__ == self_.__annotations__["error"]:
                self_.error = kvargs["error"]
            else:
                self_.error = SpacesError(**kvargs["error"])
        if "share" in kvargs:
            if type(kvargs["share"]).__name__ == self_.__annotations__["share"]:
                self_.share = kvargs["share"]
            else:
                self_.share = Share(**kvargs["share"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ShareLinks:
    """

    Attributes
    ----------
    self: SpacesLink
    space: SpacesLink
    """

    self: SpacesLink = None
    space: SpacesLink = None

    def __init__(self_, **kvargs):

        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = SpacesLink(**kvargs["self"])
        if "space" in kvargs:
            if type(kvargs["space"]).__name__ == self_.__annotations__["space"]:
                self_.space = kvargs["space"]
            else:
                self_.space = SpacesLink(**kvargs["space"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SharePatch:
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
class ShareRoleType:
    """
    Supported roles by space type:
    - Shared: consumer
    - Managed: consumer, contributor


    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Shares:
    """

    Attributes
    ----------
    data: list[Share]
    links: SharesLinks
    meta: SharesMeta
    """

    data: list[Share] = None
    links: SharesLinks = None
    meta: SharesMeta = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Share(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = SharesLinks(**kvargs["links"])
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ == self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = SharesMeta(**kvargs["meta"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SharesCreate:
    """

    Attributes
    ----------
    data: list[ShareCreate]
    """

    data: list[ShareCreate] = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [ShareCreate(**e) for e in kvargs["data"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SharesCreated:
    """

    Attributes
    ----------
    createdShares: list[ShareCreated]
    """

    createdShares: list[ShareCreated] = None

    def __init__(self_, **kvargs):

        if "createdShares" in kvargs:
            if (
                type(kvargs["createdShares"]).__name__
                == self_.__annotations__["createdShares"]
            ):
                self_.createdShares = kvargs["createdShares"]
            else:
                self_.createdShares = [
                    ShareCreated(**e) for e in kvargs["createdShares"]
                ]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SharesLinks:
    """

    Attributes
    ----------
    next: SpacesLink
    prev: SpacesLink
    self: SpacesLink
    """

    next: SpacesLink = None
    prev: SpacesLink = None
    self: SpacesLink = None

    def __init__(self_, **kvargs):

        if "next" in kvargs:
            if type(kvargs["next"]).__name__ == self_.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = SpacesLink(**kvargs["next"])
        if "prev" in kvargs:
            if type(kvargs["prev"]).__name__ == self_.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = SpacesLink(**kvargs["prev"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = SpacesLink(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SharesMeta:
    """

    Attributes
    ----------
    count: int
      The total number of Shares matching the current filter.
    """

    count: int = None

    def __init__(self_, **kvargs):

        if "count" in kvargs:
            if type(kvargs["count"]).__name__ == self_.__annotations__["count"]:
                self_.count = kvargs["count"]
            else:
                self_.count = kvargs["count"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpaceCreate:
    """

    Attributes
    ----------
    description: str
      The description of the space. Personal spaces do not have a description.
    name: str
      The name of the space. Personal spaces do not have a name.
    type: str
      The type of space such as shared, managed, and so on.
    """

    description: str = None
    name: str = None
    type: str = None

    def __init__(self_, **kvargs):

        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                == self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ == self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ == self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpaceLinks:
    """

    Attributes
    ----------
    assignments: SpacesLink
    self: SpacesLink
    """

    assignments: SpacesLink = None
    self: SpacesLink = None

    def __init__(self_, **kvargs):

        if "assignments" in kvargs:
            if (
                type(kvargs["assignments"]).__name__
                == self_.__annotations__["assignments"]
            ):
                self_.assignments = kvargs["assignments"]
            else:
                self_.assignments = SpacesLink(**kvargs["assignments"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = SpacesLink(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpaceMeta:
    """
    Information about the space settings.

    Attributes
    ----------
    actions: list[str]
      The list of actions allowed by the current user in this space.
    assignableRoles: list[str]
      The list of roles that could be assigned in this space.
    roles: list[str]
      The list of roles assigned to the current user in this space.
    """

    actions: list[str] = None
    assignableRoles: list[str] = None
    roles: list[str] = None

    def __init__(self_, **kvargs):

        if "actions" in kvargs:
            if type(kvargs["actions"]).__name__ == self_.__annotations__["actions"]:
                self_.actions = kvargs["actions"]
            else:
                self_.actions = kvargs["actions"]
        if "assignableRoles" in kvargs:
            if (
                type(kvargs["assignableRoles"]).__name__
                == self_.__annotations__["assignableRoles"]
            ):
                self_.assignableRoles = kvargs["assignableRoles"]
            else:
                self_.assignableRoles = kvargs["assignableRoles"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ == self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacePatch:
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
class SpaceTypes:
    """
    The distinct types of spaces (shared, managed, and so on).

    Attributes
    ----------
    data: list[str]
    """

    data: list[str] = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = kvargs["data"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpaceUpdate:
    """

    Attributes
    ----------
    description: str
      The description of the space. Personal spaces do not have a description.
    name: str
      The name of the space.
    ownerId: str
      The user ID of the space owner.
    """

    description: str = None
    name: str = None
    ownerId: str = None

    def __init__(self_, **kvargs):

        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                == self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ == self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ == self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesClass:
    """

    Attributes
    ----------
    data: list[Space]
    links: SpacesLinks
    meta: SpacesMeta
    """

    data: list[Space] = None
    links: SpacesLinks = None
    meta: SpacesMeta = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Space(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = SpacesLinks(**kvargs["links"])
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ == self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = SpacesMeta(**kvargs["meta"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesLinks:
    """

    Attributes
    ----------
    next: SpacesLink
    prev: SpacesLink
    self: SpacesLink
    """

    next: SpacesLink = None
    prev: SpacesLink = None
    self: SpacesLink = None

    def __init__(self_, **kvargs):

        if "next" in kvargs:
            if type(kvargs["next"]).__name__ == self_.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = SpacesLink(**kvargs["next"])
        if "prev" in kvargs:
            if type(kvargs["prev"]).__name__ == self_.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = SpacesLink(**kvargs["prev"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = SpacesLink(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesMeta:
    """

    Attributes
    ----------
    count: int
      The total number of spaces matching the current filter.
    """

    count: int = None

    def __init__(self_, **kvargs):

        if "count" in kvargs:
            if type(kvargs["count"]).__name__ == self_.__annotations__["count"]:
                self_.count = kvargs["count"]
            else:
                self_.count = kvargs["count"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesError:
    """
    An error object.

    Attributes
    ----------
    code: str
      The error code.
    detail: str
      A human-readable explanation specific to the occurrence of this problem.
    meta: SpacesErrorMeta
      Additional properties relating to the error.
    title: str
      Summary of the problem.
    """

    code: str = None
    detail: str = None
    meta: SpacesErrorMeta = None
    title: str = None

    def __init__(self_, **kvargs):

        if "code" in kvargs:
            if type(kvargs["code"]).__name__ == self_.__annotations__["code"]:
                self_.code = kvargs["code"]
            else:
                self_.code = kvargs["code"]
        if "detail" in kvargs:
            if type(kvargs["detail"]).__name__ == self_.__annotations__["detail"]:
                self_.detail = kvargs["detail"]
            else:
                self_.detail = kvargs["detail"]
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ == self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = SpacesErrorMeta(**kvargs["meta"])
        if "title" in kvargs:
            if type(kvargs["title"]).__name__ == self_.__annotations__["title"]:
                self_.title = kvargs["title"]
            else:
                self_.title = kvargs["title"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesErrorMeta:
    """
    Additional properties relating to the error.

    Attributes
    ----------
    source: SpacesErrorMetaSource
      References to the source of the error.
    """

    source: SpacesErrorMetaSource = None

    def __init__(self_, **kvargs):

        if "source" in kvargs:
            if type(kvargs["source"]).__name__ == self_.__annotations__["source"]:
                self_.source = kvargs["source"]
            else:
                self_.source = SpacesErrorMetaSource(**kvargs["source"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesErrorMetaSource:
    """
    References to the source of the error.

    Attributes
    ----------
    parameter: str
      The URI query parameter that caused the error.
    pointer: str
      A JSON pointer to the property that caused the error.
    """

    parameter: str = None
    pointer: str = None

    def __init__(self_, **kvargs):

        if "parameter" in kvargs:
            if type(kvargs["parameter"]).__name__ == self_.__annotations__["parameter"]:
                self_.parameter = kvargs["parameter"]
            else:
                self_.parameter = kvargs["parameter"]
        if "pointer" in kvargs:
            if type(kvargs["pointer"]).__name__ == self_.__annotations__["pointer"]:
                self_.pointer = kvargs["pointer"]
            else:
                self_.pointer = kvargs["pointer"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class SpacesLink:
    """

    Attributes
    ----------
    href: str
      URL that defines the resource.
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


class Spaces:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def create_filters(
        self, data: FilterSpaces = None, max_items: int = 10
    ) -> ListableResource[Space]:
        """
        Experimental
        Retrieves spaces that the current user has access to with provided space IDs or names.

        Parameters
        ----------
        data: FilterSpaces = None
          Filter criteria for one or more spaces.
        """
        warnings.warn("create_filters is experimental", UserWarning, stacklevel=2)
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/filter",
            method="POST",
            params={},
            data=data,
        )
        return ListableResource(
            response=response.json(),
            cls=Space,
            auth=self.auth,
            path="/spaces/filter",
            max_items=max_items,
            query_params={},
        )

    def get_shares_license(self) -> FineGrainedLicense:
        """
        Experimental
        Get licenses for fine-grained.

        Parameters
        ----------
        """
        warnings.warn("get_shares_license is experimental", UserWarning, stacklevel=2)
        response = self.auth.rest(
            path="/spaces/shares/license",
            method="GET",
            params={},
            data=None,
        )
        obj = FineGrainedLicense(**response.json())
        obj.auth = self.auth
        return obj

    def get_types(self) -> SpaceTypes:
        """
        Gets a list of distinct space types.

        Parameters
        ----------
        """
        response = self.auth.rest(
            path="/spaces/types",
            method="GET",
            params={},
            data=None,
        )
        obj = SpaceTypes(**response.json())
        obj.auth = self.auth
        return obj

    def delete_assignment(self, assignmentId: str, spaceId: str) -> None:
        """
        Deletes an assignment.

        Parameters
        ----------
        assignmentId: str
          The ID of the assignment to delete.
        spaceId: str
          The ID of the space of the assignment.
        """
        self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{assignmentId}", assignmentId
            ).replace("{spaceId}", spaceId),
            method="DELETE",
            params={},
            data=None,
        )

    def get_assignment(self, assignmentId: str, spaceId: str) -> Assignment:
        """
        Retrieves a single assignment by ID.

        Parameters
        ----------
        assignmentId: str
          The ID of the assignment to retrieve.
        spaceId: str
          The ID of the space of the assignment.
        """
        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{assignmentId}", assignmentId
            ).replace("{spaceId}", spaceId),
            method="GET",
            params={},
            data=None,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj

    def set_assignment(
        self, assignmentId: str, spaceId: str, data: AssignmentUpdate
    ) -> Assignment:
        """
        Experimental
        Updates a single assignment by ID. The complete list of roles must be provided.

        Parameters
        ----------
        assignmentId: str
          The ID of the assignment to update.
        spaceId: str
          The ID of the space of the assignment.
        data: AssignmentUpdate
          Attributes that the user wants to update for the specified assignment.
        """
        warnings.warn("set_assignment is experimental", UserWarning, stacklevel=2)
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{assignmentId}", assignmentId
            ).replace("{spaceId}", spaceId),
            method="PUT",
            params={},
            data=data,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj

    def delete_share(self, shareId: str, spaceId: str) -> None:
        """
        Experimental
        Deletes a Share.

        Parameters
        ----------
        shareId: str
          The ID of the share to delete.
        spaceId: str
          The ID of the space to which the share belongs.
        """
        warnings.warn("delete_share is experimental", UserWarning, stacklevel=2)
        self.auth.rest(
            path="/spaces/{spaceId}/shares/{shareId}".replace(
                "{shareId}", shareId
            ).replace("{spaceId}", spaceId),
            method="DELETE",
            params={},
            data=None,
        )

    def get_share(self, shareId: str, spaceId: str) -> Share:
        """
        Experimental
        Retrieves a single share by ID.

        Parameters
        ----------
        shareId: str
          The ID of the share to retrieve.
        spaceId: str
          The ID of the space to which the share belongs.
        """
        warnings.warn("get_share is experimental", UserWarning, stacklevel=2)
        response = self.auth.rest(
            path="/spaces/{spaceId}/shares/{shareId}".replace(
                "{shareId}", shareId
            ).replace("{spaceId}", spaceId),
            method="GET",
            params={},
            data=None,
        )
        obj = Share(**response.json())
        obj.auth = self.auth
        return obj

    def patch_share(self, shareId: str, spaceId: str, data: SharePatch) -> Share:
        """
        Experimental
        Patches (updates) a share (partially).

        Parameters
        ----------
        shareId: str
          The ID of the share to update.
        spaceId: str
          The ID of the space to which the share belongs.
        data: SharePatch

        """
        warnings.warn("patch_share is experimental", UserWarning, stacklevel=2)
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces/{spaceId}/shares/{shareId}".replace(
                "{shareId}", shareId
            ).replace("{spaceId}", spaceId),
            method="PATCH",
            params={},
            data=data,
        )
        obj = Share(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, spaceId: str) -> Space:
        """
        Retrieves a single space by ID.

        Parameters
        ----------
        spaceId: str
          The ID of the space to retrieve.
        """
        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", spaceId),
            method="GET",
            params={},
            data=None,
        )
        obj = Space(**response.json())
        obj.auth = self.auth
        return obj

    def get_spaces(
        self,
        action: str = None,
        filter: str = None,
        limit: int = 10,
        name: str = None,
        next: str = None,
        ownerId: str = None,
        prev: str = None,
        sort: str = None,
        type: str = None,
        max_items: int = 10,
    ) -> ListableResource[Space]:
        """
        Retrieves spaces that the current user has access to and match the query.

        Parameters
        ----------
        action: str = None
          Action on space. For example, "?action=publish".
        filter: str = None
          Exact match filtering on space name using SCIM. Case insensitive on attribute name. For example ?filter=name eq "MySpace" and ?filter=NAME eq "MySpace" is both valid.
        limit: int = 10
          Maximum number of spaces to return.
        name: str = None
          Space name to search and filter for. Case-insensitive open search with wildcards both as prefix and suffix. For example, "?name=fin" will get "finance", "Final" and "Griffin".
        next: str = None
          The next page cursor. Next links make use of this.
        ownerId: str = None
          Space ownerId to filter by. For example, "?ownerId=123".
        prev: str = None
          The previous page cursor. Previous links make use of this.
        sort: str = None
          Field to sort by. Prefix with +/- to indicate asc/desc. For example, "?sort=+name" to sort ascending on Name. Supported fields are "type", "name" and "createdAt".
        type: str = None
          Type(s) of space to filter. For example, "?type=managed,shared".
        """
        query_params = {}
        if action is not None:
            query_params["action"] = action
        if filter is not None:
            query_params["filter"] = filter

            warnings.warn("filter is experimental", UserWarning, stacklevel=2)
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if next is not None:
            query_params["next"] = next
        if ownerId is not None:
            query_params["ownerId"] = ownerId
        if prev is not None:
            query_params["prev"] = prev
        if sort is not None:
            query_params["sort"] = sort
        if type is not None:
            query_params["type"] = type
        response = self.auth.rest(
            path="/spaces",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Space,
            auth=self.auth,
            path="/spaces",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, data: SpaceCreate) -> Space:
        """
        Creates a space.

        Parameters
        ----------
        data: SpaceCreate
          Attributes that the user wants to set for a new space.
        """
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/spaces",
            method="POST",
            params={},
            data=data,
        )
        obj = Space(**response.json())
        obj.auth = self.auth
        return obj
