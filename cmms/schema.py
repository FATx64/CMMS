from __future__ import annotations

import graphene
from graphene_django import DjangoObjectType

from cmms.models import Agent as AgentModel


class Agent(DjangoObjectType):
    class Meta:
        model = AgentModel
        field = ("id",)


class Query(graphene.ObjectType):
    agents = graphene.List(Agent, id=graphene.Int())
    agent = graphene.Field(Agent, id=graphene.Int())

    @staticmethod
    def is_authenticated(info):
        if info.context.user.is_authenticated:
            return True
        raise RuntimeError("Not authenticated")

    def resolve_agents(self, info, **kwargs):
        if not Query.is_authenticated(info):
            return

        if kwargs:
            return AgentModel.objects.filter(**kwargs)
        return AgentModel.objects.all()

    def resolve_agent(self, info, *, id):
        if not Query.is_authenticated(info):
            return

        return AgentModel.objects.filter(id=id).first()


schema = graphene.Schema(query=Query)
