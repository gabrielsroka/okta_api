from okta.client import Client as OktaClient
import asyncio

async def main():
    async with OktaClient() as client:
        query_params = {'filter': 'status eq "SUSPENDED"'} # SUSPENDED, DEPROVISIONED, etc. see https://developer.okta.com/docs/reference/api/users/#user-properties
        users, resp, err = await client.list_users(query_params)
        while users:
            for user in users:
                print(user.profile.login, user.status) # Add more properties here.
                if user.status != 'DEPROVISIONED': # Must call deactivate_or_delete_user twice.
                    await client.deactivate_or_delete_user(user.id)
                await client.deactivate_or_delete_user(user.id)

            users, err = await resp.next() if resp.has_next() else (None, None)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
