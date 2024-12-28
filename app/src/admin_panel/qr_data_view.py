from sqladmin import ModelView

from twots_bot.models.orm.qr_data import QRData


class QRDataAdmin(ModelView, model=QRData):
    column_list = [QRData.id, QRData.qr_data, QRData.user_id]
    column_searchable_list = [QRData.qr_data]
    column_sortable_list = [QRData.id]
