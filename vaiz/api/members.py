from vaiz.api.base import BaseAPIClient
from vaiz.models import GetSpaceMembersResponse


class MembersAPIClient(BaseAPIClient):
    def get_space_members(self) -> GetSpaceMembersResponse:
        """
        Get all members in the current space.

        Bot members (AI, automation, integration bots) are excluded from the result.

        Returns:
            GetSpaceMembersResponse: The list of space members
        """
        response_data = self._make_request("getSpaceMembers", method="POST", json_data={})
        members = response_data.get("payload", {}).get("members", [])
        response_data["payload"]["members"] = [
            m for m in members if not str(m.get("kind", "")).endswith("Bot")
        ]
        return GetSpaceMembersResponse(**response_data)

