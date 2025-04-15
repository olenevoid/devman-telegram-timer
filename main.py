from dotenv import load_dotenv
from os import getenv
from ptbot import Bot
from pytimeparse import parse


load_dotenv()

TG_TOKEN = getenv('TG_TOKEN')


def render_progressbar(
        total,
        iteration,
        prefix='',
        suffix='',
        length=30,
        fill='█',
        zfill='░'
        ):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def timer(chat_id: str, delay: int, bot: Bot):
    message = 'Время вышло'
    bot.create_timer(
        delay,
        bot_reply,
        chat_id=chat_id,
        message=message,
        bot=bot)


def countdown(chat_id: str, countdown_time: int, bot: Bot):
    message_id = bot.send_message(chat_id, 'Запускаю таймер')
    bot.create_countdown(
        countdown_time,
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        total_time=countdown_time,
        bot=bot
        )


def start_timer(chat_id: str, incoming_message: str, bot: Bot):
    time = parse(incoming_message)
    if time:
        countdown(chat_id, time, bot)
        timer(chat_id, time, bot)
    else:
        bot_reply(chat_id, 'Неверный формат времени', bot)


def notify_progress(
        secs_left: int,
        chat_id: str,
        message_id: int,
        total_time: int,
        bot: Bot):
    progress_bar = render_progressbar(total_time, total_time-secs_left)
    message = f'Осталось {secs_left} секунд\n{progress_bar}'
    edit_message(chat_id, message_id, message, bot)


def edit_message(chat_id, message_id, new_message, bot: Bot):
    bot.update_message(chat_id, message_id, new_message)


def bot_reply(chat_id: str, message: str, bot: Bot):
    bot.send_message(chat_id, message)


def main():
    bot = Bot(TG_TOKEN)
    bot.reply_on_message(start_timer, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
