class DBRouter:
    bot_app_label = 'bot'
    bot_db = 'bot'
    default_db = 'default'

    def db_for_read(self, model, **hints):
        "Point all operations on bot models to 'bot' db"
        if model._meta.app_label == self.bot_app_label:
            return self.bot_db
        return self.default_db

    def db_for_write(self, model, **hints):
        "Point all operations on bot models to 'bot' db"
        if model._meta.app_label == self.bot_app_label:
            return self.bot_db
        return self.default_db

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in bot app"
        if obj1._meta.app_label == self.bot_app_label and obj2._meta.app_label == self.bot_app_label:
            return True
        elif self.bot_app_label not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_syncdb(self, db, model):
        if db == self.bot_db or model._meta.app_label == self.bot_app_label:
            return False  # we're not using syncdb on our legacy database
        else:  # but all other models/databases are fine
            return True
