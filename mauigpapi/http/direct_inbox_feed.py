# mautrix-instagram - A Matrix-Instagram puppeting bridge.
# Copyright (C) 2020 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Optional, Any

from attr import dataclass
from mautrix.types import SerializableAttrs

from .base import BaseAndroidAPI


@dataclass
class DirectInboxResponse(SerializableAttrs['DirectInboxFeedResponse']):
    status: str
    seq_id: int
    snapshot_at_ms: int
    pending_requests_total: int
    # TODO
    inbox: Any
    most_recent_inviter: Any = None


class DirectInboxAPI(BaseAndroidAPI):
    async def direct_inbox(self, cursor: Optional[str] = None, seq_id: Optional[str] = None,
                           thread_message_limit: int = 10, limit: int = 20) -> DirectInboxResponse:
        query = {
            "visual_message_return_type": "unseen",
            "cursor": cursor,
            "direction": "older" if cursor else None,
            "seq_id": seq_id,
            "thread_message_limit": thread_message_limit,
            "persistentBadging": "true",
            "limit": limit,
        }
        query = {k: v for k, v in query.items() if v is not None}
        url = (self.url / "api/v1/direct_v2/inbox/").with_query(query)
        resp = await self.http.get(url, headers=self.headers)
        return DirectInboxResponse.deserialize(await self.handle_response(resp))