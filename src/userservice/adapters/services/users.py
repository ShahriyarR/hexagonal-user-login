from uuid import UUID

from eventsourcing.application import AggregateNotFound, Application

from userservice.domain.model.aggregate import User
from userservice.domain.model.exceptions import UserAccountNotFoundError


class UsersService(Application):
    def register_user(self, full_name: str, email: str) -> UUID:
        user = User.register(
            full_name=full_name,
            email=email,
        )
        self.save(user)
        return user.id

    def get_user(self, user_id: UUID) -> User:
        try:
            aggregate = self.repository.get(user_id)
        except AggregateNotFound as err:
            raise UserAccountNotFoundError(user_id) from err
        else:
            assert isinstance(aggregate, User)
            return aggregate
