class CatalogError(Exception):
    pass


class DuplicateIDError(CatalogError):  # дубликат id
    pass


class IncorrectEntityError(CatalogError):  # некорректная сущность
    pass


class NotFoundObjectError(CatalogError):  # не найден объект
    pass


class UnsupportedVersionError(CatalogError):  # неподдерживаемая версия формата
    pass


class DamagedFileError(CatalogError):  # поврежденный файл
    pass
