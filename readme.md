Telegram bot that give access to document such passport etc. by document type or document owner. User can save
documents.  
Firstly I wanted to store documents on file manager. Finally, will store on telegram cloud.

ToDo:

- Temporary store date(various menu options, document types, document owners names, documents) in project itself.
    - Create local db
- Tests
- Implement del_docs method
- Refactor ~~message_reply~~, ~~show_docs~~ methods
- Type hints: ~~send_start_info~~, ~~message_reply~~, ~~save_docs~~, delete_docs
- Write exceptions: ~~save_docs~~
- Add default doc_types, saving docs by default doc types, adding doc types