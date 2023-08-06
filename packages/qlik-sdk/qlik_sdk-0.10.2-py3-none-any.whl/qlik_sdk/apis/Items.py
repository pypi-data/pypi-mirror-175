# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services 0.478.8

from __future__ import annotations

import warnings
from dataclasses import asdict, dataclass

from ..auth import Auth, Config
from ..listable import ListableResource


@dataclass
class ItemResultResponseBody:
    """
    An item.

    Attributes
    ----------
    actions: list[str]
      The actions that the user can perform on the item.
    collectionIds: list[str]
      The ID of the collections that the item has been added to.
    createdAt: str
      The RFC3339 datetime when the item was created.
    creatorId: str
      The ID of the user who created the item. This is only populated if the JWT contains a userId.
    description: str
    id: str
      The item's unique identifier.
    isFavorited: bool
      The flag that indicates if item is in the user's favorites collection.
    itemViews: ItemViewsResponseBody
    links: ItemLinksResponseBody
    meta: ItemMetaResponseBody
      Item metadata and computed fields.
    name: str
    ownerId: str
      The ID of the user who owns the item.
    resourceAttributes: object
    resourceCreatedAt: str
      The RFC3339 datetime when the resource that the item references was created.
    resourceCustomAttributes: object
    resourceId: str
      The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceLink: str
      The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceReloadEndTime: str
      The RFC3339 datetime when the resource last reload ended.
    resourceReloadStatus: str
      If the resource last reload was successful or not.
    resourceSize: ItemsResourceSizeResponseBody
    resourceSubType: str
      Optional field defining the item's subtype, if any.
    resourceType: str
      The case-sensitive string defining the item's type.
    resourceUpdatedAt: str
      The RFC3339 datetime when the resource that the item references was last updated.
    spaceId: str
      The space's unique identifier.
    tenantId: str
      The ID of the tenant that owns the item. This is populated using the JWT.
    thumbnailId: str
      The item thumbnail's unique identifier. This is optional for internal resources.
    updatedAt: str
      The RFC3339 datetime when the item was last updated.
    updaterId: str
      ID of the user who last updated the item. This is only populated if the JWT contains a userId.
    """

    actions: list[str] = None
    collectionIds: list[str] = None
    createdAt: str = None
    creatorId: str = None
    description: str = None
    id: str = None
    isFavorited: bool = None
    itemViews: ItemViewsResponseBody = None
    links: ItemLinksResponseBody = None
    meta: ItemMetaResponseBody = None
    name: str = None
    ownerId: str = None
    resourceAttributes: object = None
    resourceCreatedAt: str = None
    resourceCustomAttributes: object = None
    resourceId: str = None
    resourceLink: str = None
    resourceReloadEndTime: str = None
    resourceReloadStatus: str = None
    resourceSize: ItemsResourceSizeResponseBody = None
    resourceSubType: str = None
    resourceType: str = None
    resourceUpdatedAt: str = None
    spaceId: str = None
    tenantId: str = None
    thumbnailId: str = None
    updatedAt: str = None
    updaterId: str = None

    def __init__(self_, **kvargs):

        if "actions" in kvargs:
            if type(kvargs["actions"]).__name__ == self_.__annotations__["actions"]:
                self_.actions = kvargs["actions"]
            else:
                self_.actions = kvargs["actions"]
        if "collectionIds" in kvargs:
            if (
                type(kvargs["collectionIds"]).__name__
                == self_.__annotations__["collectionIds"]
            ):
                self_.collectionIds = kvargs["collectionIds"]
            else:
                self_.collectionIds = kvargs["collectionIds"]
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ == self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "creatorId" in kvargs:
            if type(kvargs["creatorId"]).__name__ == self_.__annotations__["creatorId"]:
                self_.creatorId = kvargs["creatorId"]
            else:
                self_.creatorId = kvargs["creatorId"]
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
        if "isFavorited" in kvargs:
            if (
                type(kvargs["isFavorited"]).__name__
                == self_.__annotations__["isFavorited"]
            ):
                self_.isFavorited = kvargs["isFavorited"]
            else:
                self_.isFavorited = kvargs["isFavorited"]
        if "itemViews" in kvargs:
            if type(kvargs["itemViews"]).__name__ == self_.__annotations__["itemViews"]:
                self_.itemViews = kvargs["itemViews"]
            else:
                self_.itemViews = ItemViewsResponseBody(**kvargs["itemViews"])
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ItemLinksResponseBody(**kvargs["links"])
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ == self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = ItemMetaResponseBody(**kvargs["meta"])
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
        if "resourceAttributes" in kvargs:
            if (
                type(kvargs["resourceAttributes"]).__name__
                == self_.__annotations__["resourceAttributes"]
            ):
                self_.resourceAttributes = kvargs["resourceAttributes"]
            else:
                self_.resourceAttributes = kvargs["resourceAttributes"]
        if "resourceCreatedAt" in kvargs:
            if (
                type(kvargs["resourceCreatedAt"]).__name__
                == self_.__annotations__["resourceCreatedAt"]
            ):
                self_.resourceCreatedAt = kvargs["resourceCreatedAt"]
            else:
                self_.resourceCreatedAt = kvargs["resourceCreatedAt"]
        if "resourceCustomAttributes" in kvargs:
            if (
                type(kvargs["resourceCustomAttributes"]).__name__
                == self_.__annotations__["resourceCustomAttributes"]
            ):
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
            else:
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
        if "resourceId" in kvargs:
            if (
                type(kvargs["resourceId"]).__name__
                == self_.__annotations__["resourceId"]
            ):
                self_.resourceId = kvargs["resourceId"]
            else:
                self_.resourceId = kvargs["resourceId"]
        if "resourceLink" in kvargs:
            if (
                type(kvargs["resourceLink"]).__name__
                == self_.__annotations__["resourceLink"]
            ):
                self_.resourceLink = kvargs["resourceLink"]
            else:
                self_.resourceLink = kvargs["resourceLink"]
        if "resourceReloadEndTime" in kvargs:
            if (
                type(kvargs["resourceReloadEndTime"]).__name__
                == self_.__annotations__["resourceReloadEndTime"]
            ):
                self_.resourceReloadEndTime = kvargs["resourceReloadEndTime"]
            else:
                self_.resourceReloadEndTime = kvargs["resourceReloadEndTime"]
        if "resourceReloadStatus" in kvargs:
            if (
                type(kvargs["resourceReloadStatus"]).__name__
                == self_.__annotations__["resourceReloadStatus"]
            ):
                self_.resourceReloadStatus = kvargs["resourceReloadStatus"]
            else:
                self_.resourceReloadStatus = kvargs["resourceReloadStatus"]
        if "resourceSize" in kvargs:
            if (
                type(kvargs["resourceSize"]).__name__
                == self_.__annotations__["resourceSize"]
            ):
                self_.resourceSize = kvargs["resourceSize"]
            else:
                self_.resourceSize = ItemsResourceSizeResponseBody(
                    **kvargs["resourceSize"]
                )
        if "resourceSubType" in kvargs:
            if (
                type(kvargs["resourceSubType"]).__name__
                == self_.__annotations__["resourceSubType"]
            ):
                self_.resourceSubType = kvargs["resourceSubType"]
            else:
                self_.resourceSubType = kvargs["resourceSubType"]
        if "resourceType" in kvargs:
            if (
                type(kvargs["resourceType"]).__name__
                == self_.__annotations__["resourceType"]
            ):
                self_.resourceType = kvargs["resourceType"]
            else:
                self_.resourceType = kvargs["resourceType"]
        if "resourceUpdatedAt" in kvargs:
            if (
                type(kvargs["resourceUpdatedAt"]).__name__
                == self_.__annotations__["resourceUpdatedAt"]
            ):
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
            else:
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
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
        if "thumbnailId" in kvargs:
            if (
                type(kvargs["thumbnailId"]).__name__
                == self_.__annotations__["thumbnailId"]
            ):
                self_.thumbnailId = kvargs["thumbnailId"]
            else:
                self_.thumbnailId = kvargs["thumbnailId"]
        if "updatedAt" in kvargs:
            if type(kvargs["updatedAt"]).__name__ == self_.__annotations__["updatedAt"]:
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]
        if "updaterId" in kvargs:
            if type(kvargs["updaterId"]).__name__ == self_.__annotations__["updaterId"]:
                self_.updaterId = kvargs["updaterId"]
            else:
                self_.updaterId = kvargs["updaterId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)

    def get_collections(
        self,
        limit: int = None,
        name: str = None,
        next: str = None,
        prev: str = None,
        query: str = None,
        sort: str = None,
        type: str = None,
        max_items: int = 10,
    ) -> ListableResource[CollectionResultResponseBody]:
        """
        Returns the collections of an item.
        Finds and returns the collections of an item. This endpoint does not return the user's favorites collection.


        Parameters
        ----------
        limit: int = None
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        name: str = None
          The case-sensitive string used to search for a collection by name.
        next: str = None
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.
        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        query: str = None
          The case-insensitive string used to search for a resource by name or description.
        sort: str = None
          The property of a resource to sort on (default sort is +createdAt). The supported properties are createdAt, updatedAt, and name. A property must be prefixed by + or   - to indicate ascending or descending sort order respectively.
        type: str = None
          The case-sensitive string used to search for a collection by type.
        """
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if query is not None:
            query_params["query"] = query
        if sort is not None:
            query_params["sort"] = sort
        if type is not None:
            query_params["type"] = type
        response = self.auth.rest(
            path="/items/{itemId}/collections".replace("{itemId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=CollectionResultResponseBody,
            auth=self.auth,
            path="/items/{itemId}/collections".replace("{itemId}", self.id),
            max_items=max_items,
            query_params=query_params,
        )

    def get_publisheditems(
        self,
        limit: int = None,
        next: str = None,
        prev: str = None,
        resourceType: str = None,
        sort: str = None,
        max_items: int = 10,
    ) -> ListableResource[CollectionResultResponseBody]:
        """
        Returns published items for a given item.
        Finds and returns the published items for a given item.


        Parameters
        ----------
        limit: int = None
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        next: str = None
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.
        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        resourceType: str = None
          The case-sensitive string used to search for an item by resourceType.
        sort: str = None
          The property of a resource to sort on (default sort is +createdAt). The supported properties are createdAt, updatedAt, and name. A property must be prefixed by + or   - to indicate ascending or descending sort order respectively.
        """
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev
        if resourceType is not None:
            query_params["resourceType"] = resourceType
        if sort is not None:
            query_params["sort"] = sort
        response = self.auth.rest(
            path="/items/{itemId}/publisheditems".replace("{itemId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=CollectionResultResponseBody,
            auth=self.auth,
            path="/items/{itemId}/publisheditems".replace("{itemId}", self.id),
            max_items=max_items,
            query_params=query_params,
        )

    def delete(self) -> None:
        """
        Experimental
        Deletes an item.
        Deletes an item and removes the item from all collections.


        Parameters
        ----------
        """
        warnings.warn("delete is experimental", UserWarning, stacklevel=2)
        self.auth.rest(
            path="/items/{itemId}".replace("{itemId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def set(self, data: ItemsUpdateItemRequestBody) -> ItemResultResponseBody:
        """
        Experimental
        Updates an item.
        Updates an item. Omitted and unsupported fields are ignored. To unset a field, provide the field's zero value.


        Parameters
        ----------
        data: ItemsUpdateItemRequestBody

        """
        warnings.warn("set is experimental", UserWarning, stacklevel=2)
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/items/{itemId}".replace("{itemId}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self


@dataclass
class ItemsCreateItemRequestBody:
    """

    Attributes
    ----------
    description: str
    name: str
    resourceAttributes: object
    resourceCreatedAt: str
      The RFC3339 datetime when the resource that the item references was created.
    resourceCustomAttributes: object
    resourceId: str
      The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceLink: str
      The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceSubType: str
      Optional field defining the item's subtype, if any.
    resourceType: str
      The case-sensitive string defining the item's type.
    resourceUpdatedAt: str
      The RFC3339 datetime when the resource that the item references was last updated.
    spaceId: str
      The space's unique identifier.
    thumbnailId: str
      The item thumbnail's unique identifier. This is optional for internal resources.
    """

    description: str = None
    name: str = None
    resourceAttributes: object = None
    resourceCreatedAt: str = None
    resourceCustomAttributes: object = None
    resourceId: str = None
    resourceLink: str = None
    resourceSubType: str = None
    resourceType: str = None
    resourceUpdatedAt: str = None
    spaceId: str = None
    thumbnailId: str = None

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
        if "resourceAttributes" in kvargs:
            if (
                type(kvargs["resourceAttributes"]).__name__
                == self_.__annotations__["resourceAttributes"]
            ):
                self_.resourceAttributes = kvargs["resourceAttributes"]
            else:
                self_.resourceAttributes = kvargs["resourceAttributes"]
        if "resourceCreatedAt" in kvargs:
            if (
                type(kvargs["resourceCreatedAt"]).__name__
                == self_.__annotations__["resourceCreatedAt"]
            ):
                self_.resourceCreatedAt = kvargs["resourceCreatedAt"]
            else:
                self_.resourceCreatedAt = kvargs["resourceCreatedAt"]
        if "resourceCustomAttributes" in kvargs:
            if (
                type(kvargs["resourceCustomAttributes"]).__name__
                == self_.__annotations__["resourceCustomAttributes"]
            ):
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
            else:
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
        if "resourceId" in kvargs:
            if (
                type(kvargs["resourceId"]).__name__
                == self_.__annotations__["resourceId"]
            ):
                self_.resourceId = kvargs["resourceId"]
            else:
                self_.resourceId = kvargs["resourceId"]
        if "resourceLink" in kvargs:
            if (
                type(kvargs["resourceLink"]).__name__
                == self_.__annotations__["resourceLink"]
            ):
                self_.resourceLink = kvargs["resourceLink"]
            else:
                self_.resourceLink = kvargs["resourceLink"]
        if "resourceSubType" in kvargs:
            if (
                type(kvargs["resourceSubType"]).__name__
                == self_.__annotations__["resourceSubType"]
            ):
                self_.resourceSubType = kvargs["resourceSubType"]
            else:
                self_.resourceSubType = kvargs["resourceSubType"]
        if "resourceType" in kvargs:
            if (
                type(kvargs["resourceType"]).__name__
                == self_.__annotations__["resourceType"]
            ):
                self_.resourceType = kvargs["resourceType"]
            else:
                self_.resourceType = kvargs["resourceType"]
        if "resourceUpdatedAt" in kvargs:
            if (
                type(kvargs["resourceUpdatedAt"]).__name__
                == self_.__annotations__["resourceUpdatedAt"]
            ):
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
            else:
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ == self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        if "thumbnailId" in kvargs:
            if (
                type(kvargs["thumbnailId"]).__name__
                == self_.__annotations__["thumbnailId"]
            ):
                self_.thumbnailId = kvargs["thumbnailId"]
            else:
                self_.thumbnailId = kvargs["thumbnailId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsListItemCollectionsResponseBody:
    """
    ListItemCollectionsResponseBody result type

    Attributes
    ----------
    data: list[CollectionResultResponseBody]
    links: CollectionsLinksResponseBody
    """

    data: list[CollectionResultResponseBody] = None
    links: CollectionsLinksResponseBody = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [CollectionResultResponseBody(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = CollectionsLinksResponseBody(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsListItemsResponseBody:
    """
    ListItemsResponseBody result type

    Attributes
    ----------
    data: list[ItemResultResponseBody]
    links: ItemsLinksResponseBody
    """

    data: list[ItemResultResponseBody] = None
    links: ItemsLinksResponseBody = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [ItemResultResponseBody(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ItemsLinksResponseBody(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsSettingsPatch:
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
class ItemsSettingsResponseBody:
    """

    Attributes
    ----------
    usageMetricsEnabled: bool
      Decides if the usage metrics will be shown in the hub UI.
    """

    usageMetricsEnabled: bool = True

    def __init__(self_, **kvargs):

        if "usageMetricsEnabled" in kvargs:
            if (
                type(kvargs["usageMetricsEnabled"]).__name__
                == self_.__annotations__["usageMetricsEnabled"]
            ):
                self_.usageMetricsEnabled = kvargs["usageMetricsEnabled"]
            else:
                self_.usageMetricsEnabled = kvargs["usageMetricsEnabled"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsUpdateItemRequestBody:
    """

    Attributes
    ----------
    description: str
    name: str
    resourceAttributes: object
    resourceCustomAttributes: object
    resourceId: str
      The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceLink: str
      The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
    resourceSubType: str
      Optional field defining the item's subtype, if any.
    resourceType: str
      The case-sensitive string defining the item's type.
    resourceUpdatedAt: str
      The RFC3339 datetime when the resource that the item references was last updated.
    spaceId: str
      The space's unique identifier.
    thumbnailId: str
      The item thumbnail's unique identifier. This is optional for internal resources.
    """

    description: str = None
    name: str = None
    resourceAttributes: object = None
    resourceCustomAttributes: object = None
    resourceId: str = None
    resourceLink: str = None
    resourceSubType: str = None
    resourceType: str = None
    resourceUpdatedAt: str = None
    spaceId: str = None
    thumbnailId: str = None

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
        if "resourceAttributes" in kvargs:
            if (
                type(kvargs["resourceAttributes"]).__name__
                == self_.__annotations__["resourceAttributes"]
            ):
                self_.resourceAttributes = kvargs["resourceAttributes"]
            else:
                self_.resourceAttributes = kvargs["resourceAttributes"]
        if "resourceCustomAttributes" in kvargs:
            if (
                type(kvargs["resourceCustomAttributes"]).__name__
                == self_.__annotations__["resourceCustomAttributes"]
            ):
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
            else:
                self_.resourceCustomAttributes = kvargs["resourceCustomAttributes"]
        if "resourceId" in kvargs:
            if (
                type(kvargs["resourceId"]).__name__
                == self_.__annotations__["resourceId"]
            ):
                self_.resourceId = kvargs["resourceId"]
            else:
                self_.resourceId = kvargs["resourceId"]
        if "resourceLink" in kvargs:
            if (
                type(kvargs["resourceLink"]).__name__
                == self_.__annotations__["resourceLink"]
            ):
                self_.resourceLink = kvargs["resourceLink"]
            else:
                self_.resourceLink = kvargs["resourceLink"]
        if "resourceSubType" in kvargs:
            if (
                type(kvargs["resourceSubType"]).__name__
                == self_.__annotations__["resourceSubType"]
            ):
                self_.resourceSubType = kvargs["resourceSubType"]
            else:
                self_.resourceSubType = kvargs["resourceSubType"]
        if "resourceType" in kvargs:
            if (
                type(kvargs["resourceType"]).__name__
                == self_.__annotations__["resourceType"]
            ):
                self_.resourceType = kvargs["resourceType"]
            else:
                self_.resourceType = kvargs["resourceType"]
        if "resourceUpdatedAt" in kvargs:
            if (
                type(kvargs["resourceUpdatedAt"]).__name__
                == self_.__annotations__["resourceUpdatedAt"]
            ):
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
            else:
                self_.resourceUpdatedAt = kvargs["resourceUpdatedAt"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ == self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        if "thumbnailId" in kvargs:
            if (
                type(kvargs["thumbnailId"]).__name__
                == self_.__annotations__["thumbnailId"]
            ):
                self_.thumbnailId = kvargs["thumbnailId"]
            else:
                self_.thumbnailId = kvargs["thumbnailId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class Link:
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


@dataclass
class CollectionLinksResponseBody:
    """

    Attributes
    ----------
    items: Link
    self: Link
    """

    items: Link = None
    self: Link = None

    def __init__(self_, **kvargs):

        if "items" in kvargs:
            if type(kvargs["items"]).__name__ == self_.__annotations__["items"]:
                self_.items = kvargs["items"]
            else:
                self_.items = Link(**kvargs["items"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionMetaResponseBody:
    """
    Collection metadata and computed fields.

    Attributes
    ----------
    items: ItemsResultResponseBody
      Multiple items.
    """

    items: ItemsResultResponseBody = None

    def __init__(self_, **kvargs):

        if "items" in kvargs:
            if type(kvargs["items"]).__name__ == self_.__annotations__["items"]:
                self_.items = kvargs["items"]
            else:
                self_.items = ItemsResultResponseBody(**kvargs["items"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionResultResponseBody:
    """
    A collection.

    Attributes
    ----------
    createdAt: str
      The RFC3339 datetime when the collection was created.
    creatorId: str
      The ID of the user who created the collection. This property is only populated if the JWT contains a userId.
    description: str
    id: str
      The collection's unique identifier.
    itemCount: int
      The number of items that have been added to the collection.
    links: CollectionLinksResponseBody
    meta: CollectionMetaResponseBody
      Collection metadata and computed fields.
    name: str
    tenantId: str
      The ID of the tenant that owns the collection. This property is populated by using JWT.
    type: str
      The collection's type.
    updatedAt: str
      The RFC3339 datetime when the collection was last updated.
    updaterId: str
      The ID of the user who last updated the collection. This property is only populated if the JWT contains a userId.
    """

    createdAt: str = None
    creatorId: str = None
    description: str = None
    id: str = None
    itemCount: int = None
    links: CollectionLinksResponseBody = None
    meta: CollectionMetaResponseBody = None
    name: str = None
    tenantId: str = None
    type: str = None
    updatedAt: str = None
    updaterId: str = None

    def __init__(self_, **kvargs):

        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ == self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "creatorId" in kvargs:
            if type(kvargs["creatorId"]).__name__ == self_.__annotations__["creatorId"]:
                self_.creatorId = kvargs["creatorId"]
            else:
                self_.creatorId = kvargs["creatorId"]
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
        if "itemCount" in kvargs:
            if type(kvargs["itemCount"]).__name__ == self_.__annotations__["itemCount"]:
                self_.itemCount = kvargs["itemCount"]
            else:
                self_.itemCount = kvargs["itemCount"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = CollectionLinksResponseBody(**kvargs["links"])
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ == self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = CollectionMetaResponseBody(**kvargs["meta"])
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ == self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
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
        if "updaterId" in kvargs:
            if type(kvargs["updaterId"]).__name__ == self_.__annotations__["updaterId"]:
                self_.updaterId = kvargs["updaterId"]
            else:
                self_.updaterId = kvargs["updaterId"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class CollectionsLinksResponseBody:
    """

    Attributes
    ----------
    item: Link
    next: Link
    prev: Link
    self: Link
    """

    item: Link = None
    next: Link = None
    prev: Link = None
    self: Link = None

    def __init__(self_, **kvargs):

        if "item" in kvargs:
            if type(kvargs["item"]).__name__ == self_.__annotations__["item"]:
                self_.item = kvargs["item"]
            else:
                self_.item = Link(**kvargs["item"])
        if "next" in kvargs:
            if type(kvargs["next"]).__name__ == self_.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs:
            if type(kvargs["prev"]).__name__ == self_.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemLinksResponseBody:
    """

    Attributes
    ----------
    collections: Link
    open: Link
    self: Link
    thumbnail: Link
    """

    collections: Link = None
    open: Link = None
    self: Link = None
    thumbnail: Link = None

    def __init__(self_, **kvargs):

        if "collections" in kvargs:
            if (
                type(kvargs["collections"]).__name__
                == self_.__annotations__["collections"]
            ):
                self_.collections = kvargs["collections"]
            else:
                self_.collections = Link(**kvargs["collections"])
        if "open" in kvargs:
            if type(kvargs["open"]).__name__ == self_.__annotations__["open"]:
                self_.open = kvargs["open"]
            else:
                self_.open = Link(**kvargs["open"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        if "thumbnail" in kvargs:
            if type(kvargs["thumbnail"]).__name__ == self_.__annotations__["thumbnail"]:
                self_.thumbnail = kvargs["thumbnail"]
            else:
                self_.thumbnail = Link(**kvargs["thumbnail"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemMetaResponseBody:
    """
    Item metadata and computed fields.

    Attributes
    ----------
    actions: list[str]
      The actions that the user can perform on the item.
    collections: list[ItemTagResponseBody]
      An array of collections that the item is part of.
    isFavorited: bool
      The flag that indicates if item is in the user's favorites collection.
    tags: list[ItemTagResponseBody]
      An array of tags that the item is part of.
    """

    actions: list[str] = None
    collections: list[ItemTagResponseBody] = None
    isFavorited: bool = None
    tags: list[ItemTagResponseBody] = None

    def __init__(self_, **kvargs):

        if "actions" in kvargs:
            if type(kvargs["actions"]).__name__ == self_.__annotations__["actions"]:
                self_.actions = kvargs["actions"]
            else:
                self_.actions = kvargs["actions"]
        if "collections" in kvargs:
            if (
                type(kvargs["collections"]).__name__
                == self_.__annotations__["collections"]
            ):
                self_.collections = kvargs["collections"]
            else:
                self_.collections = [
                    ItemTagResponseBody(**e) for e in kvargs["collections"]
                ]
        if "isFavorited" in kvargs:
            if (
                type(kvargs["isFavorited"]).__name__
                == self_.__annotations__["isFavorited"]
            ):
                self_.isFavorited = kvargs["isFavorited"]
            else:
                self_.isFavorited = kvargs["isFavorited"]
        if "tags" in kvargs:
            if type(kvargs["tags"]).__name__ == self_.__annotations__["tags"]:
                self_.tags = kvargs["tags"]
            else:
                self_.tags = [ItemTagResponseBody(**e) for e in kvargs["tags"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemTagResponseBody:
    """
    Holds basic information about a tag or collection.

    Attributes
    ----------
    id: str
      The ID of the tag/collection.
    name: str
      The name of the tag/collection.
    """

    id: str = None
    name: str = None

    def __init__(self_, **kvargs):

        if "id" in kvargs:
            if type(kvargs["id"]).__name__ == self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ == self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemViewsResponseBody:
    """

    Attributes
    ----------
    total: int
      Total number of views the resource got during the last 28 days.
    trend: float
      Trend in views over the last 4 weeks.
    unique: int
      Number of unique users who viewed the resource during the last 28 days.
    usedBy: int
      Number of apps this dataset is used in (datasets only).
    week: list[ItemViewsWeeksResponseBody]
    """

    total: int = None
    trend: float = None
    unique: int = None
    usedBy: int = None
    week: list[ItemViewsWeeksResponseBody] = None

    def __init__(self_, **kvargs):

        if "total" in kvargs:
            if type(kvargs["total"]).__name__ == self_.__annotations__["total"]:
                self_.total = kvargs["total"]
            else:
                self_.total = kvargs["total"]
        if "trend" in kvargs:
            if type(kvargs["trend"]).__name__ == self_.__annotations__["trend"]:
                self_.trend = kvargs["trend"]
            else:
                self_.trend = kvargs["trend"]
        if "unique" in kvargs:
            if type(kvargs["unique"]).__name__ == self_.__annotations__["unique"]:
                self_.unique = kvargs["unique"]
            else:
                self_.unique = kvargs["unique"]
        if "usedBy" in kvargs:
            if type(kvargs["usedBy"]).__name__ == self_.__annotations__["usedBy"]:
                self_.usedBy = kvargs["usedBy"]
            else:
                self_.usedBy = kvargs["usedBy"]
        if "week" in kvargs:
            if type(kvargs["week"]).__name__ == self_.__annotations__["week"]:
                self_.week = kvargs["week"]
            else:
                self_.week = [ItemViewsWeeksResponseBody(**e) for e in kvargs["week"]]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemViewsWeeksResponseBody:
    """

    Attributes
    ----------
    start: str
      The RFC3339 datetime representing the start of the referenced week.
    total: int
      Total number of views the resource got during the referenced week.
    unique: int
      Number of unique users who viewed the resource during the referenced week.
    """

    start: str = None
    total: int = None
    unique: int = None

    def __init__(self_, **kvargs):

        if "start" in kvargs:
            if type(kvargs["start"]).__name__ == self_.__annotations__["start"]:
                self_.start = kvargs["start"]
            else:
                self_.start = kvargs["start"]
        if "total" in kvargs:
            if type(kvargs["total"]).__name__ == self_.__annotations__["total"]:
                self_.total = kvargs["total"]
            else:
                self_.total = kvargs["total"]
        if "unique" in kvargs:
            if type(kvargs["unique"]).__name__ == self_.__annotations__["unique"]:
                self_.unique = kvargs["unique"]
            else:
                self_.unique = kvargs["unique"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsLinksResponseBody:
    """

    Attributes
    ----------
    collection: Link
    next: Link
    prev: Link
    self: Link
    """

    collection: Link = None
    next: Link = None
    prev: Link = None
    self: Link = None

    def __init__(self_, **kvargs):

        if "collection" in kvargs:
            if (
                type(kvargs["collection"]).__name__
                == self_.__annotations__["collection"]
            ):
                self_.collection = kvargs["collection"]
            else:
                self_.collection = Link(**kvargs["collection"])
        if "next" in kvargs:
            if type(kvargs["next"]).__name__ == self_.__annotations__["next"]:
                self_.next = kvargs["next"]
            else:
                self_.next = Link(**kvargs["next"])
        if "prev" in kvargs:
            if type(kvargs["prev"]).__name__ == self_.__annotations__["prev"]:
                self_.prev = kvargs["prev"]
            else:
                self_.prev = Link(**kvargs["prev"])
        if "self" in kvargs:
            if type(kvargs["self"]).__name__ == self_.__annotations__["self"]:
                self_.self = kvargs["self"]
            else:
                self_.self = Link(**kvargs["self"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsResourceSizeResponseBody:
    """

    Attributes
    ----------
    appFile: float
      Size of the app on disk in bytes.
    appMemory: float
      Size of the app in memory in bytes.
    """

    appFile: float = None
    appMemory: float = None

    def __init__(self_, **kvargs):

        if "appFile" in kvargs:
            if type(kvargs["appFile"]).__name__ == self_.__annotations__["appFile"]:
                self_.appFile = kvargs["appFile"]
            else:
                self_.appFile = kvargs["appFile"]
        if "appMemory" in kvargs:
            if type(kvargs["appMemory"]).__name__ == self_.__annotations__["appMemory"]:
                self_.appMemory = kvargs["appMemory"]
            else:
                self_.appMemory = kvargs["appMemory"]
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


@dataclass
class ItemsResultResponseBody:
    """
    Multiple items.

    Attributes
    ----------
    data: list[ItemResultResponseBody]
    links: ItemsLinksResponseBody
    """

    data: list[ItemResultResponseBody] = None
    links: ItemsLinksResponseBody = None

    def __init__(self_, **kvargs):

        if "data" in kvargs:
            if type(kvargs["data"]).__name__ == self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [ItemResultResponseBody(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ == self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = ItemsLinksResponseBody(**kvargs["links"])
        for k0, v in kvargs.items():
            k = k0.replace("-", "_")
            if k not in getattr(self_, "__annotations__", {}):
                self_.__setattr__(k, v)


class Items:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_settings(self) -> ItemsSettingsResponseBody:
        """
        Experimental
        Returns tenant specific settings.
        Finds and returns the settings for the current tenant.


        Parameters
        ----------
        """
        warnings.warn("get_settings is experimental", UserWarning, stacklevel=2)
        response = self.auth.rest(
            path="/items/settings",
            method="GET",
            params={},
            data=None,
        )
        obj = ItemsSettingsResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def patch_settings(self, data: ItemsSettingsPatch) -> ItemsSettingsResponseBody:
        """
        Experimental
        Patches tenant specific settings.
        Updates the settings provided in the patch body.

        Parameters
        ----------
        data: ItemsSettingsPatch

        """
        warnings.warn("patch_settings is experimental", UserWarning, stacklevel=2)
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/items/settings",
            method="PATCH",
            params={},
            data=data,
        )
        obj = ItemsSettingsResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def get(self, itemId: str) -> ItemResultResponseBody:
        """
        Returns an item.
        Finds and returns an item.


        Parameters
        ----------
        itemId: str
          The item's unique identifier
        """
        response = self.auth.rest(
            path="/items/{itemId}".replace("{itemId}", itemId),
            method="GET",
            params={},
            data=None,
        )
        obj = ItemResultResponseBody(**response.json())
        obj.auth = self.auth
        return obj

    def get_items(
        self,
        collectionId: str = None,
        createdByUserId: str = None,
        id: str = None,
        limit: int = None,
        name: str = None,
        next: str = None,
        notCreatedByUserId: str = None,
        notOwnerId: str = None,
        ownerId: str = None,
        prev: str = None,
        query: str = None,
        resourceId: str = None,
        resourceIds: str = None,
        resourceLink: str = None,
        resourceSubType: str = None,
        resourceType: str = None,
        shared: bool = None,
        sort: str = None,
        spaceId: str = None,
        noActions: bool = False,
        max_items: int = 10,
    ) -> ListableResource[ItemResultResponseBody]:
        """
        Retrieves items that the user has access to.
        Finds and returns items that the user has access to.


        Parameters
        ----------
        collectionId: str = None
          The collection's unique identifier.
        createdByUserId: str = None
          User's unique identifier.
        id: str = None
          The item's unique identifier.
        limit: int = None
          The maximum number of resources to return for a request. The limit must be an integer between 1 and 100 (inclusive).
        name: str = None
          The case-insensitive string used to search for a resource by name.
        next: str = None
          The cursor to the next page of resources. Provide either the next or prev cursor, but not both.
        notCreatedByUserId: str = None
          User's unique identifier.
        notOwnerId: str = None
          Owner identifier.
        ownerId: str = None
          Owner identifier.
        prev: str = None
          The cursor to the previous page of resources. Provide either the next or prev cursor, but not both.
        query: str = None
          The case-insensitive string used to search for a resource by name or description.
        resourceId: str = None
          The case-sensitive string used to search for an item by resourceId. If resourceId is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
        resourceIds: str = None
          The case-sensitive strings used to search for an item by resourceIds. The maximum number of resourceIds it supports is 100. If resourceIds is provided, then resourceType must be provided. For example '?resourceIds=appId1,appId2'
        resourceLink: str = None
          The case-sensitive string used to search for an item by resourceLink. If resourceLink is provided, then resourceType must be provided. Provide either the resourceId or resourceLink, but not both.
        resourceSubType: str = None
          the case-sensitive string used to filter items by resourceSubType(s). For example '?resourceSubType=chart-monitoring,qix-df,qvd'
        resourceType: str = None
          The case-sensitive string used to filter items by resourceType(s). For example '?resourceType=app,qvapp'
        shared: bool = None
          Whether or not to return items in a shared space.
        sort: str = None
          The property of a resource to sort on (default sort is +createdAt). The supported properties are createdAt, updatedAt, and name. A property must be prefixed by + or   - to indicate ascending or descending sort order respectively.
        spaceId: str = None
          The space's unique identifier (supports \'personal\' as spaceId).
        noActions: bool = False
          If set to true, the user's available actions for each item will not be evaluated meaning the actions-array will be omitted from the response (reduces response time).

        """
        query_params = {}
        if collectionId is not None:
            query_params["collectionId"] = collectionId
        if createdByUserId is not None:
            query_params["createdByUserId"] = createdByUserId
        if id is not None:
            query_params["id"] = id
        if limit is not None:
            query_params["limit"] = limit
        if name is not None:
            query_params["name"] = name
        if next is not None:
            query_params["next"] = next
        if notCreatedByUserId is not None:
            query_params["notCreatedByUserId"] = notCreatedByUserId
        if notOwnerId is not None:
            query_params["notOwnerId"] = notOwnerId
        if ownerId is not None:
            query_params["ownerId"] = ownerId
        if prev is not None:
            query_params["prev"] = prev
        if query is not None:
            query_params["query"] = query
        if resourceId is not None:
            query_params["resourceId"] = resourceId
        if resourceIds is not None:
            query_params["resourceIds"] = resourceIds
        if resourceLink is not None:
            query_params["resourceLink"] = resourceLink
        if resourceSubType is not None:
            query_params["resourceSubType"] = resourceSubType
        if resourceType is not None:
            query_params["resourceType"] = resourceType
        if shared is not None:
            query_params["shared"] = shared
        if sort is not None:
            query_params["sort"] = sort
        if spaceId is not None:
            query_params["spaceId"] = spaceId
        if noActions is not None:
            query_params["noActions"] = noActions
        response = self.auth.rest(
            path="/items",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=ItemResultResponseBody,
            auth=self.auth,
            path="/items",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, data: ItemsCreateItemRequestBody) -> ItemResultResponseBody:
        """
        Experimental
        Creates and returns a new item.
        Creates and returns a new item.
        An item references an internal or external resource. A resource cannot be both internal and external.

        `resourceType` must be provided for both internal and external items.

        `resourceId` must be provided for internal items.

        `resourceLink` must be provided for external items.

        For a given tenant, an item's resourceId or resourceLink is unique.


        Parameters
        ----------
        data: ItemsCreateItemRequestBody

        """
        warnings.warn("create is experimental", UserWarning, stacklevel=2)
        if data is not None:
            try:
                data = asdict(data)
            except:
                data = data
        response = self.auth.rest(
            path="/items",
            method="POST",
            params={},
            data=data,
        )
        obj = ItemResultResponseBody(**response.json())
        obj.auth = self.auth
        return obj
