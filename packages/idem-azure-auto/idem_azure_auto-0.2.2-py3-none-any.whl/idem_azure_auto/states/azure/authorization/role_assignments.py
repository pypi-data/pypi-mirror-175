"""
Autogenerated using `pop-create-idem <https://gitlab.com/saltstack/pop/pop-create-idem>`__


"""
import copy
import uuid
from collections import OrderedDict
from typing import Any
from typing import Dict


__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    scope: str,
    role_definition_id: str,
    principal_id: str,
    resource_id: str = None,
    role_assignment_name: str = None,
) -> Dict[str, Any]:
    r"""
    **Autogenerated function**

    Create or update Role Assignments

    Args:
        name(str): The identifier for this state.
        scope(str): The scope of the role assignment to create. The scope can be any REST resource instance.
         For example, use '/subscriptions/{subscription-id}/' for a subscription,
          '/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}' for a resource group,
           and '/subscriptions/{subscription-id}/resourceGroups/{resource-group-name}/providers/{resource-provider}/{resource-type}/{resource-name}' for a resource.
        role_definition_id(str): The role definition ID used in the role assignment.
        principal_id(str): The principal ID assigned to the role. This maps to the ID inside the Active Directory. It can point to a user, service principal, or security group.
        resource_id(str, optional): Role Assignment resource id on Azure.
        role_assignment_name(str, optional): A GUID for the role assignment to create. The name must be unique and different for each role assignment. This will be automatically generated if not specified.

    Returns:
        Dict

    Examples:

        .. code-block:: sls

            resource_is_present:
              azure.authorization.role_assignments.present:
                - name: value
                - scope: value
                - role_assignment_name: value
    """
    result = {
        "name": name,
        "result": True,
        "old_state": None,
        "new_state": None,
        "comment": [],
    }
    response_get = None
    if role_assignment_name:
        if resource_id is None:
            resource_id = f"{scope}/providers/Microsoft.Authorization/roleAssignments/{role_assignment_name}"
        response_get = await hub.exec.request.json.get(
            ctx,
            url=f"{hub.exec.azure.URL}/{resource_id}?api-version=2015-07-01",
            success_codes=[200],
        )

    if response_get is None or not response_get["result"]:
        if response_get is None:
            role_assignment_name = uuid.uuid4()
        if response_get["status"] == 404:
            if ctx.get("test", False):
                # Return a proposed state by Idem state --test
                result[
                    "new_state"
                ] = hub.tool.azure.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "name": name,
                        "scope": scope,
                        "role_assignment_name": role_assignment_name,
                        "resource_id": resource_id,
                        "role_definition_id": role_definition_id,
                        "principal_id": principal_id,
                    },
                )
                result["comment"].append(
                    f"Would create azure.authorization.role_assignments '{name}'"
                )
                return result
            else:
                # PUT operation to create a resource
                payload = hub.tool.azure.authorization.role_assignments.convert_present_to_raw_role_assignments(
                    role_definition_id=role_definition_id,
                    principal_id=principal_id,
                )
                response_put = await hub.exec.request.json.put(
                    ctx,
                    url=f"{hub.exec.azure.URL}{resource_id}?api-version=2015-07-01",
                    success_codes=[201],
                    json=payload,
                )

                if not response_put["result"]:
                    hub.log.debug(
                        f"Could not create azure.authorization.role_assignments {response_put['comment']} {response_put['ret']}"
                    )
                    result["comment"] = [response_put["comment"], response_put["ret"]]
                    result["result"] = False
                    return result

                result[
                    "new_state"
                ] = hub.tool.azure.authorization.role_assignments.convert_raw_role_assignments_to_present(
                    resource=response_put["ret"],
                    idem_resource_name=name,
                    role_assignment_name=role_assignment_name,
                    resource_id=resource_id,
                )
                result["comment"].append(
                    f"Created azure.authorization.role_assignments '{name}'"
                )
                return result

        else:
            hub.log.debug(
                f"Could not get azure.authorization.role_assignments {response_get['comment']} {response_get['ret']}"
            )
            result["result"] = False
            result["comment"] = [response_get["comment"], response_get["ret"]]
            return result

    else:
        existing_resource = response_get["ret"]
        result[
            "old_state"
        ] = hub.tool.azure.authorization.role_assignments.convert_raw_role_assignments_to_present(
            resource=existing_resource,
            idem_resource_name=name,
            role_assignment_name=role_assignment_name,
            resource_id=resource_id,
        )
        # No role assignment property can be updated without resource re-creation.
        result["comment"].append(
            f"azure.authorization.role_assignments '{name}' has no property to be updated."
        )
        result["new_state"] = copy.deepcopy(result["old_state"])
        return result


async def absent(
    hub, ctx, name: str, scope: str, role_assignment_name: str, resource_id: str = None
) -> Dict[str, Any]:
    r"""
    **Autogenerated function**

    Delete Role Assignments

    Args:
        name(str): The identifier for this state.
        scope(str, optional): The scope of the role assignment to delete.
        role_assignment_name(str, optional): The name of the role assignment to delete.
        resource_id(str, optional): Role assignment resource id on Azure. Either resource_id or a combination of scope
         and role_assignment_name need to be specified. Idem will automatically consider a resource as absent if both
          options are not specified.

    Returns:
        Dict

    Examples:

        .. code-block:: sls

            resource_is_absent:
              azure.authorization.role_assignments.absent:
                - name: value
                - scope: value
                - role_assignment_name: value
    """

    result = dict(name=name, result=True, comment=[], old_state=None, new_state=None)
    if scope is not None and role_assignment_name is not None:
        constructed_resource_id = f"{scope}/providers/Microsoft.Authorization/roleAssignments/{role_assignment_name}"
        if resource_id is not None and resource_id != constructed_resource_id:
            result["result"] = False
            result["comment"].append(
                f"azure.authorization.role_assignments '{name}' resource_id {resource_id} does not match the constructed resource id"
            )
            return result
        resource_id = constructed_resource_id
    response_get = await hub.exec.request.json.get(
        ctx,
        url=f"{hub.exec.azure.URL}/{resource_id}?api-version=2015-07-01",
        success_codes=[200],
    )
    if response_get["result"]:
        result[
            "old_state"
        ] = hub.tool.azure.authorization.role_assignments.convert_raw_role_assignments_to_present(
            resource=response_get["ret"],
            idem_resource_name=name,
            role_assignment_name=role_assignment_name,
            resource_id=resource_id,
        )
        if ctx.get("test", False):
            result["comment"].append(
                f"Would delete azure.authorization.role_assignments '{name}'"
            )
            return result
        response_delete = await hub.exec.request.raw.delete(
            ctx,
            url=f"{hub.exec.azure.URL}/{resource_id}?api-version=2015-07-01",
            success_codes=[200, 204],
        )

        if not response_delete["result"]:
            hub.log.debug(
                f"Could not delete azure.authorization.role_assignments '{name}' {response_delete['comment']} {response_delete['ret']}"
            )
            result["result"] = False
            result["comment"] = [response_delete["comment"], response_delete["ret"]]
            return result

        result["comment"].append(
            f"Deleted azure.authorization.role_assignments '{name}'"
        )
        return result
    elif response_get["status"] == 404:
        # If Azure returns 'Not Found' error, it means the resource has been absent.
        result["comment"].append(
            f"azure.authorization.role_assignments '{name}' already absent"
        )
        return result
    else:
        hub.log.debug(
            f"Could not get azure.authorization.role_assignments '{name}' {response_get['comment']} {response_get['ret']}"
        )
        result["result"] = False
        result["comment"] = [response_get["comment"], response_get["ret"]]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""
    **Autogenerated function**

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function


    List all Role Assignments under the same subscription


    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe azure.authorization.role_assignments
    """

    result = {}
    subscription_id = ctx.acct.subscription_id
    uri_parameters = OrderedDict({"roleAssignments": "role_assignment_name"})
    async for page_result in hub.tool.azure.request.paginate(
        ctx,
        url=f"{hub.exec.azure.URL}/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleAssignments?api-version=2015-07-01",
        success_codes=[200],
    ):
        resource_list = page_result.get("value")
        if resource_list:
            for resource in resource_list:
                resource_id = resource["id"]
                uri_parameter_values = hub.tool.azure.uri.get_parameter_value_in_dict(
                    resource_id, uri_parameters
                )
                resource_translated = hub.tool.azure.authorization.role_assignments.convert_raw_role_assignments_to_present(
                    resource=resource,
                    idem_resource_name=resource_id,
                    resource_id=resource_id,
                    **uri_parameter_values,
                )
                result[resource["id"]] = {
                    f"azure.authorization.role_assignments.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in resource_translated.items()
                    ]
                }
    return result
