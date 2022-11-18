import okta.client
import asyncio

client: okta.client.Client

async def main():
    global client
    async with okta.client.Client() as client:
        # SUSPENDED, DEPROVISIONED, etc. see https://developer.okta.com/docs/reference/api/users/#user-properties
        async for user in get_users(search='status eq "SUSPENDED"'):
            print(user.id, user.profile.login, user.status) # Add more properties here.
            if user.status != 'DEPROVISIONED': # Must call deactivate_or_delete_user twice.
                await client.deactivate_or_delete_user(user.id)
            await client.deactivate_or_delete_user(user.id)

async def get_users(**params):
    users, resp, _ = await client.list_users(params)
    while users:
        for user in users:
            yield user
        users, _ = await resp.next() if resp.has_next() else (None, None)

asyncio.run(main())
