from __future__ import annotations

import graphene
from graphene_django import DjangoObjectType

from cmms.models import Agent as AgentModel


class Agent(DjangoObjectType):
    class Meta:
        model = AgentModel


class Query(graphene.ObjectType):
    agents = graphene.List(Agent)

    @staticmethod
    def is_authenticated(info):
        if info.context.user.is_authenticated:
            return True
        raise RuntimeError("Not authenticated")

    def resolve_agents(self, info, **kwargs):
        if not Query.is_authenticated(info):
            return

        return AgentModel.objects.all()


schema = graphene.Schema(query=Query)
