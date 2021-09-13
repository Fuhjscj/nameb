import vkquick as vq
from tortoise import Tortoise
from title_changer.misc import load_settings
from title_changer.commands import app as bp
from title_changer import changers

import asyncio

from async_cron.job import CronJob
from async_cron.schedule import Scheduler

import threading

SETINGS = load_settings()

app = vq.App(
    debug=SETINGS.debug,
    prefixes=['.н ', '!н '],
    filter=vq.filters.Dynamic(lambda ctx: ctx.msg.from_id == SETINGS.admin_id)
)

api = vq.API(SETINGS.access_token)
vq.InvalidArgumentConfig.prefix_sign = "⚠"

app.add_package(bp)



class SheluderThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.SETINGS = load_settings()
        self.loop = asyncio.new_event_loop()
        self.api = vq.API(self.SETINGS.access_token)

    async def intit_tortoise(self):
        await Tortoise.init(
            db_url=self.SETINGS.db_url,
            modules={"models": ["title_changer.tortoise_models"]}
        )
        try:
            await Tortoise.generate_schemas(safe=True)
        except:
            pass

    def run(self):
        asyncio.set_event_loop(self.loop)
        msh = Scheduler(locale="ru_RU", loop=self.loop)
        msh.add_job(
            CronJob(name='day').every(1).day.at(self.SETINGS.day_change_time).go(changers.update_name_day, api=self.api)
        )
        msh.add_job(
            CronJob(name='nigth').every(1).day.at(self.SETINGS.nigth_change_time).go(changers.update_name_nigth, api=self.api)
        )
        self.loop.run_until_complete(self.intit_tortoise())
        self.loop.run_until_complete(msh.start())



@app.on_startup()
async def on_startup(*args, **kwargs):
    await Tortoise.init(
        db_url=SETINGS.db_url,
        modules={"models": ["title_changer.tortoise_models"]}
    )
    try:
        await Tortoise.generate_schemas(safe=True)
    except:
        pass


@app.on_shutdown()
async def on_shutdown(*args, **kwargs):
    await Tortoise.close_connections()


if __name__ == "__main__":
    SheluderThread(daemon=True).start()
    app.run(api, build_autodoc=False)