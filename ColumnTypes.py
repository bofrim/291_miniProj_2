class ColumnTypes:
    types = None

    @staticmethod
    def setTypes(newTypes):
        ColumnTypes.types = newTypes
        print '********************* Types Set ***************************'
        print ColumnTypes.types

    @staticmethod
    def getTypes():
        return ColumnTypes.types