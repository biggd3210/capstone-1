# # class TravelParty(db.Model):
# #     """tabel of travel parties"""

# #     __tablename__ = "travelparties"

# #     id = db.Column(
# #         db.Integer,
# #         primary_key=True
# #     )
    
# #     name = db.Column(
# #         db.Text,
# #         nullable=False
# #     )


# class TravelParty_User(db.Model):
#     """relational table to connect users into travel parties."""

#     __tablename__ = 'travelparties_users'

#     id = db.Column(
#         db.Integer,
#         primary_key=True
#     )

#     user_id = db.Column(
#         db.Integer,
#         db.ForeignKey(
#             "users.id",
#             ondelete="cascade"
#         )
#     )
    
#     travelparty_id = db.Column(
#         db.Integer,
#         db.ForeignKey(
#             'travelparties.id',
#             ondelete="cascade"
#         )
#     )