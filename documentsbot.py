"""
Documents bot
"""
from dataclasses import dataclass
from telebot import TeleBot, types
from credentials import bot_token

bot = TeleBot(bot_token, parse_mode=None)


@dataclass
class Document:
    name: str
    type: str
    owner_name: str
    message_id: int


initial_menu = ['Save document', 'Delete document', 'Saved documents']
docs = []
options = ['By document owner name', 'By document type']
owners = set()
document_types = {'passport'}


def inline_keyboard_markup(items: [list[str], set[str]]) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for item in items:
        btn = types.InlineKeyboardButton(text=item, callback_data=item)
        markup.add(btn)
    return markup


@bot.message_handler(commands=['start'])
def send_start_menu(message):
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=inline_keyboard_markup(initial_menu))


@bot.message_handler(content_types=['text'])
def text_message_handler(message):
    bot.send_message(message.chat.id, 'Right now there is no text handlers')


@bot.callback_query_handler(func=lambda call: call.data in initial_menu)
def initial_menu_(call: types.CallbackQuery):
    if call.data == 'Save document':
        bot.register_next_step_handler(call.message, save_docs)
    if call.data == 'Delete document':
        bot.send_message(call.message.chat.id, 'Choose doc that should be deleted?',
                         reply_markup=inline_keyboard_markup([f'delete {doc.name}' for doc in docs]))
    if call.data == 'Saved documents':
        bot.send_message(call.message.chat.id, 'How represent the docs?', reply_markup=inline_keyboard_markup(options))


@bot.callback_query_handler(func=lambda call: call.data in options)
def options_(call: types.CallbackQuery):
    if call.data == 'By document owner name':
        bot.send_message(call.message.chat.id, 'Whose documents show?', reply_markup=inline_keyboard_markup(owners))
    if call.data == 'By document type':
        bot.send_message(call.message.chat.id, 'Which types of documents show?',
                         reply_markup=inline_keyboard_markup(document_types))


@bot.callback_query_handler(func=lambda call: call.data in owners)
def documents_by_owner(call: types.CallbackQuery):
    bot.send_message(call.message.chat.id, 'Choose document',
                     reply_markup=filter_docs(lambda doc: doc.owner_name == call.data))


@bot.callback_query_handler(func=lambda call: call.data in document_types)
def documents_by_type(call: types.CallbackQuery):
    bot.send_message(call.message.chat.id, 'Choose document',
                     reply_markup=filter_docs(lambda doc: doc.type == call.data))

@bot.callback_query_handler(func=lambda call: call.data in document_types)
def documents_by_type(call: types.CallbackQuery):
    bot.send_message(call.message.chat.id, 'Choose document',
                     reply_markup=filter_docs(lambda doc: doc.type == call.data))


def save_docs(message: types.Message) -> None:
    try:
        docs.append(form_doc(message))
        bot.send_message(message.chat.id, 'Документ успешно сохранён')
    except MessageDontContainDocumentException:
        bot.send_message(message.chat.id, 'Бот сохраняет только файлы')
    except DocumentCaptionIncorrectFormatException:
        bot.send_message(message.chat.id,
                         'Document caption have incorrect format, should contain document description in '
                         'format:"Document_Owner_name Document_Type"')


class MessageDontContainDocumentException(Exception):
    """Raised when message dont contain document"""
    pass


class DocumentCaptionIncorrectFormatException(Exception):
    """Raised when message caption have incorrect format, should contain document description in format:
    'Document_Owner_name Document_Type' """
    pass


def form_doc(message: types.Message) -> Document:
    if message.document is None:
        raise MessageDontContainDocumentException
    if message.caption is None or len(message.caption.split()) != 2:
        raise DocumentCaptionIncorrectFormatException
    doc_name = message.document.file_name
    doc_type = message.caption.split()[-1]
    owner_name = ' '.join(message.caption.split()[:-1])
    message_id = message.id
    owners.add(owner_name)
    document_types.add(doc_type)
    return Document(doc_name, doc_type, owner_name, message_id)


def filter_docs(filter_=lambda doc: doc) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    for item in [d for d in docs if filter_(d)]:
        btn = types.InlineKeyboardButton(text=item.name, callback_data=item.name)
        markup.add(btn)
    return markup


bot.polling(none_stop=True)
