# Generated by Django 5.1.3 on 2024-12-03 17:55

from django.db import migrations, models


def populate_roles(apps, schema_editor):
    MailTemplate = apps.get_model("mail", "MailTemplate")
    Event = apps.get_model("event", "Event")

    mapping = {
        "submission.new": "ack_template",
        "submission.state.accepted": "accept_template",
        "submission.state.rejected": "reject_template",
        "schedule.new": "update_template",
        "question.reminder": "question_template",
    }
    for role, field in mapping.items():
        MailTemplate.objects.all().filter(
            pk__in=Event.objects.all().values_list(field, flat=True)
        ).update(role=role)


def unset_roles(apps, schema_editor):
    MailTemplate = apps.get_model("mail", "MailTemplate")
    MailTemplate.objects.all().update(role=None)


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0036_alter_event_header_image_alter_event_logo"),
        ("mail", "0012_queuedmail_submissions"),
    ]

    operations = [
        migrations.AddField(
            model_name="mailtemplate",
            name="role",
            field=models.CharField(default=None, max_length=30, null=True),
        ),
        migrations.AlterUniqueTogether(
            name="mailtemplate",
            unique_together={("event", "role")},
        ),
        migrations.RunPython(
            populate_roles,
            reverse_code=unset_roles,
        ),
    ]
