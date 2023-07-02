from __future__ import annotations

import graphene
from graphene_django import DjangoObjectType

from cmms.models import Agent as AgentModel


class Agent(DjangoObjectType):
    class Meta:
        model = AgentModel


class Query(graphene.ObjectType):
    agents = graphene.List(Agent)

    def resolve_agents(self, info, **kwargs):
        return AgentModel.objects.all()


schema = graphene.Schema(query=Query)
