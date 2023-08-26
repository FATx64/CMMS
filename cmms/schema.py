from __future__ import annotations

import graphene
from graphene_django import DjangoObjectType

from cmms.core.models import Agent as AgentModel
from cmms.core.models import Equipment as EquipmentModel
from cmms.core.models import Sparepart as SparepartModel


class Equipment(DjangoObjectType):
    class Meta:
        model = EquipmentModel
        field = ("id",)


class Agent(DjangoObjectType):
    class Meta:
        model = AgentModel
        field = ("id",)


class Sparepart(DjangoObjectType):
    class Meta:
        model = SparepartModel
        field = ("id", "equipment")


class Query(graphene.ObjectType):
    agents = graphene.List(Agent, id=graphene.Int())
    agent = graphene.Field(Agent, id=graphene.Int())
    sparepart = graphene.Field(Sparepart, id=graphene.Int())

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

    def resolve_sparepart(self, info, *, id):
        if not Query.is_authenticated(info):
            return

        return SparepartModel.objects.filter(id=id).first()


schema = graphene.Schema(query=Query)
