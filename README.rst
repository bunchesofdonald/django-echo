===========
django-echo
===========

Django library for creating skills for the Amazon Echo (Alexa)

===============
Getting Started
===============

django-echo is mainly composed of three classes:

- ``echo.skill.EchoSkill``: A subclass of Django's generic.View that handles routing intents and dealing with request data.
- ``echo.request.EchoRequest``: A small wrapper around the JSON data in the request from Amazon.
- ``echo.response.EchoResponse``: A subclass of Django's http.HttpResponse that knows how to generate a valid Amazon Echo response.


Creating a Skill
----------------
A skill is a class that subclasses EchoSkill that provides intent handlers::

    from echo.skill import EchoSkill

    class HoroscopeSkill(EchoSkill):
        def get_horoscope(self, request, sign):
            # Ignore the sign because astrology is bunk.
            return self.respond(
                "Today you need to act first and ask questions later!",
                card=None,
                should_end_session=True
            )


On the Amazon side you would setup an intent called ``GetHoroscope`` that has
a ``sign`` slot, and when that intent is called this ``get_horoscope`` method
will be called with the slot data.

The ``self.respond`` is a helper method that essentially just acts as a
pass-through to ``EchoResponse``. You can also use SSML directly and
EchoResponse will set the response up correctly::

    self.respond("<speak>Today you need to ask questions first and act later!</speak>")

Then you just need to wire the skill up to your urls.py::

    from django.conf.urls import url

    from .views import HoroscopeSkill

    urlpatterns = [
        url(
            regex=r'^horoscope/$',
            view=HoroscopeSkill.as_view(),
            name='horoscope_skill'
        )
    ]


Responding With A Card
----------------------
EchoSkill provides a helper to create a simple card::

        return self.respond(
            "What alexa should say",
            card=self.create_simple_card("The card title", "The card's content")
        )


Session Handling
----------------
EchoSkill sets ``self.request`` to an instance of EchoRequest (it also saves
the http request to ``self.http_request``.) EchoRequest provides the session
attributes via a ``session`` attribute::

    sign = self.request.session.get('sign')

    request.session.update({
        'has_requested_horoscope': True
    })

If you use ``EchoSkill.respond`` this session data will be automatically
attached to the response, otherwise you'll need to pass it when creating the
response::

        return EchoResponse("Output text", session=self.request.session)
