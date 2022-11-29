import okta.client
import asyncio

limit = 75 # 15, 35, or 75. see https://developer.okta.com/docs/reference/rl-additional-limits/#concurrent-rate-limits

client: okta.client.Client
users: list
counts = [0] * limit

async def main():
    global client
    async with okta.client.Client() as client:
        print('get users')
        global users
        users, resp, _ = await client.list_users()
        for i in range(2):
            more_users, _ = await resp.next() if resp.has_next() else (None, None)
            users.extend(more_users)
        users = users[0:525]

        print('start tasks')
        tasks = (task(i) for i in range(limit))
        await asyncio.gather(*tasks)

        counts.sort()
        for i in counts:
            print(i)
        print(sum(counts))

async def task(i):
    while users:
        user = users.pop()
        gs, r, _ = await client.list_user_groups(user.id)
        counts[i] += 1
        # print(i, user.id) # , ', '.join([g.id for g in gs]))

asyncio.run(main())
