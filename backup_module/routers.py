# backup_module/routers.py

class LogRouter:
    """
    Controla dónde deben ir las operaciones de lectura/escritura y migraciones
    para el modelo BackupLog (que pertenece a la app 'backup_module').
    """
    
    # Especificamos qué aplicaciones manejará este router
    route_app_labels = {'backup_module'} 

    def db_for_read(self, model, **hints):
        """Redirige las lecturas (SELECT) a la BD de logs."""
        if model._meta.app_label in self.route_app_labels:
            return 'log_db'
        return 'default'

    def db_for_write(self, model, **hints):
        """Redirige las escrituras (INSERT/UPDATE/DELETE) a la BD de logs."""
        if model._meta.app_label in self.route_app_labels:
            return 'log_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite que el modelo BackupLog (en log_db) tenga una clave foránea 
        relacionada con el modelo User (que está en default).
        """
        if obj1._meta.app_label in self.route_app_labels or \
           obj2._meta.app_label in self.route_app_labels:
            return True 
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Controla en qué base de datos se pueden ejecutar las migraciones:
        - Las migraciones de 'backup_module' SÓLO pueden ir a 'log_db'.
        - Las migraciones de otras apps NO pueden ir a 'log_db'.
        """
        if app_label in self.route_app_labels:
            return db == 'log_db'
        elif db == 'log_db':
            return False 
        return True