class ColumnTypes:
    types = None

    @staticmethod
    def setTypes(newTypes):
        ColumnTypes.types = newTypes

    @staticmethod
    def getType(attr):
        if attr in ColumnTypes.types:
            return ColumnTypes.types[attr]
        else:
            return "TEXT"