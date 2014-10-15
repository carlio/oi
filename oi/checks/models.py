from django.db import models
from checks.triggers import TRIGGERS


def _trigger_choices():
    return [(name, TRIGGERS[name][1]) for name in TRIGGERS.keys()]


class Query(models.Model):
    name = models.CharField(max_length=200)
    query = models.TextField()

    def __unicode__(self):
        return self.name


class Check(models.Model):
    name = models.CharField(max_length=200)
    query = models.ForeignKey(Query)
    trigger = models.CharField(max_length=100, choices=_trigger_choices()),
    trigger_arg = models.DecimalField(max_digits=8, decimal_places=3)

    def __unicode__(self):
        return self.name


class Trip(models.Model):
    # note: this cannot be called "check" due to a bug in Django:
    # https://code.djangoproject.com/ticket/23615
    the_check = models.ForeignKey(Check)
    created = models.DateTimeField(auto_now_add=True)
    resolved = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        status = 'resolved' if self.resolved is not None else 'unresolved'
        return '%s at %s [%s]' % (self.check.name, self.created, status)
