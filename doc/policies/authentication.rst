.. _authentication_policies:

Authentication policies
-----------------------

.. index:: authentication policies

The scope *authentication* gives you more detailed
possibilities to authenticate the user or to define
what happens during authentication.

Technically the authentication policies apply
to the REST API :ref:`rest_validate` and are checked
using :ref:`code_policy` and
:ref:`policy_decorators`.

The following actions are available in the scope
*authentication*:

.. _otppin_policy:

otppin
~~~~~~

type: ``string``

This action defines how the fixed password part during
authentication should be validated.
Each token has its own OTP PIN, but the administrator can choose
how the authentication should be processed:

``otppin=tokenpin``

   This is the default behaviour. The user needs to
   pass the OTP PIN concatenated with the OTP value.

``otppin=userstore``

   The user needs to pass the user store password
   concatenated with the OTP value. It does not matter
   if the OTP PIN is set or not.
   If the user is located in an Active Directory the user
   needs to pass their domain password together with the
   OTP value.

.. note:: The domain password is checked with an LDAP
   bind right at the moment of authentication.
   So if the user is locked or the password was
   changed authentication will fail.

``otppin=none``

   The user does not have to pass any fixed password.
   Authentication is only done via the OTP value.

.. _passthru_policy:

passthru
~~~~~~~~

.. index:: passthru, migration

type: ``string``

If the user has no token assigned, they will be authenticated against the
userstore or the given RADIUS configuration.
Meaning the user needs to provide the LDAP/SQL password or valid credentials
for the RADIUS server.

.. note:: This is a good way to do a smooth enrollment.
   Users having a token enrolled will have to use the
   token, users not having a token, yet, will be able
   to authenticate with their domain password.

   It is also a way to do smooth migrations from other OTP systems.
   The authentication request of users without a token is forwarded to the
   specified RADIUS server.

.. note:: The passthru policy overrides the authorization policy
   for :ref:`tokentype_policy`. This means a user may authenticate due
   to the passthru policy (since they have no token)
   although a tokentype policy is active!

.. warning:: If the user has the right to delete their tokens in the selfservice
   portal, the user could delete all their tokens and then authenticate with
   their static password again.

passthru_assign
~~~~~~~~~~~~~~~

.. index:: passthru, migration

type: ``string``

This policy is only evaluated, if the policy ``passthru`` is set.
If the user is authenticated against a RADIUS server, then privacyIDEA
splits the sent password into PIN and OTP value and tries to find an unassigned token,
that is in the user's realm by using the OTP value. If it can identify this token, it assigns this
token to the user and sets the sent PIN.

The policy is configured with a string value, which contains

* the position of the PIN
* the OTP length and
* the number of OTP values tested for each unassigned token (optional, default=100).

Examples are

* ``8:pin`` would be an eight digit OTP value followed by the PIN
* ``pin:6:10000`` would be the PIN followed by an 6 digit OTP value, 10.000
  otp values would be checked for each token.

.. note:: This method can be used to automatically migrated tokens from an old system
   to privacyIDEA. The administrator needs to import all seeds of the old tokens
   and put the tokens in the user's realm.

.. warning:: This can be very time consuming if the OTP values to check is set too high!


.. _passonnotoken:

passOnNoToken
~~~~~~~~~~~~~

.. index:: passOnNoToken

type: ``bool``

If the user has no token assigned an authentication request
for this user will always be true.

.. warning:: Only use this if you know exactly what
   you are doing.

passOnNoUser
~~~~~~~~~~~~

.. index:: passOnNoUser

type: ``bool``

If the user does not exist, the authentication request is successful.

.. warning:: Only use this if you know exactly what you are doing.


.. _smstext:

smstext
~~~~~~~

.. index:: SMS policy, SMS text

type: ``string``

This is the text that is sent via SMS to the user trying to
authenticate with an SMS token. This can contain the tags *<otp>* and *<serial>*.
Texts containing whitespaces must be enclosed in single quotes.

Starting with version 2.20 you can use the tag *{challenge}*. This will add
the challenge data that was passed in the first authentication request in the
challenge parameter. This could contain banking transaction data.

Starting with version 3.6 the `smstext` can contain a lot more tags similar to the
policy :ref:`emailtext`:

  * {otp} or *<otp>* the One-Time-Password
  * {serial} or *<serial>* the serial number of the token.
  * {user} the given name of the token owner.
  * {givenname} the given name of the token owner.
  * {surname} the surname of the token owner.
  * {username} the loginname of the token owner.
  * {userrealm} the realm of the token owner.
  * {tokentype} the type of the token.
  * {recipient_givenname} the given name of the recipient.
  * {recipient_surname} the surname of the recipient.
  * {time} the current server time in the format HH:MM:SS.
  * {date} the current server date in the format YYYY-MM-DD

In the :ref:`sms_gateway_config` the tag *{otp}* will be replaced by the custom
message, set with this policy.

Default: *<otp>*

.. note:: The length of an SMS is limited to 140 characters due to the definition of SMS.
   You should take care, that the *smstext* does not exceed this limit. SMS gateways could
   reject too long messages or the delivery could fail.

.. note:: Some apps may be able to handle incoming OTPs as a so called
   `origin-bound one-time code <https://github.com/wicg/sms-one-time-codes>`_
   in the format::

     Your OTP is {otp}
     @privacyidea.mydomain.com #{otp}


smsautosend
~~~~~~~~~~~

.. index:: SMS automatic resend

type: ``bool``

A new OTP value will be sent via SMS if the user authenticated
successfully with their SMS token. Thus the user does not
have to trigger a new SMS when they want to login again.

.. _emailtext:

emailtext
~~~~~~~~~

.. index:: EMail policy, Email text

type: ``string``

This is the text that is sent via Email to be used with Email Token. This
text should contain the OTP tag.

The text can contain the following tags, that will be filled:

  * {otp} or *<otp>* the One-Time-Password
  * {serial} or *<serial>* the serial number of the token.
  * {user} the given name of the token owner.
  * {givenname} the given name of the token owner.
  * {surname} the surname of the token owner.
  * {username} the loginname of the token owner.
  * {userrealm} the realm of the token owner.
  * {tokentype} the type of the token.
  * {recipient_givenname} the given name of the recipient.
  * {recipient_surname} the surname of the recipient.
  * {time} the current server time in the format HH:MM:SS.
  * {date} the current server date in the format YYYY-MM-DD

Starting with version 2.20 you can use the tag *{challenge}*. This will add
the challenge data that was passed in the first authentication request in the
challenge parameter. This could contain banking transaction data.

Default: *<otp>*

You can also provide the filename to an email template. The filename must be prefixed with
``file:`` like ``file:/etc/privacyidea/emailtemplate.html``. The template is
an HTML file.

.. note:: If a message text is supplied directly, the email is sent as plain text.
   If the email template is read from a file, a HTML-only email is sent instead.

emailsubject
~~~~~~~~~~~~

.. index:: Email policy, Email subject

type: ``string``

This is the subject of the Email sent by the Email Token.
You can use the same tags as mentioned in ``emailtext``.

Default: Your OTP

emailautosend
~~~~~~~~~~~~~

.. index:: Email policy

type: ``bool``

If set, a new OTP Email will be sent, when successfully authenticated with an
Email Token.


.. _policy_mangle:

mangle
~~~~~~

.. index:: Mangle authentication request, Mangle policy

type: ``string``

The ``mangle`` policy can mangle the authentication request data before they
are processed. Meaning the parameters ``user``, ``pass`` and ``realm`` can be
modified prior to authentication.

This is useful if either information needs to be stripped or added to such a
parameter.
To accomplish that, the mangle policy can do a regular expression search and
replace using the keyword *user*, *pass* (password) and *realm*.

A valid action could look like this::

   action: mangle=user/.*(.{4})/user\\1/

This would modify a username like "userwithalongname" to "username", since it
would use the last four characters of the given username ("name") and prepend
the fixed string "user".

This way you can add, remove or modify the contents of the three parameters.
For more information on the regular expressions see [#pythonre]_.

The mangling happens *after* the user resolving as described in :ref:`relate_realm`.

.. note:: This means that you can not mangle a non-existing user or a non-existing realm.

.. note:: You must escape the backslash as **\\\\** to refer to the found
   substrings.

**Example**: A policy to remove whitespace characters from the realm name would
look like this::

   action: mangle=realm/\\s//

**Example**: If you want to authenticate the user only by the OTP value, no
matter what OTP PIN they enter, a policy might look like this::

   action: mangle=pass/.*(.{6})/\\1/

**Example**: If you want to strip a string from the front of a username, for
example to have "admin_username" resolve to just "username", it would look like
this::

   action: mangle=user/admin_(.*)/\\1/

.. _policy_challenge_response:

challenge_response
~~~~~~~~~~~~~~~~~~

type: ``string``

This is a list of token types for which challenge response can
be used during authentication. The list is separated by whitespaces like
*"hotp totp"*.


.. _policy_diable_token_types:

disable_token_types
~~~~~~~~~~~~~~~~~~~~

type: ``string``

This is a list of token types that are not allowed to be used during authentication.
The list is separated by whitespaces like *"hotp totp"*.

.. _policy_change_pin_via_validate:

force_challenge_response
~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: force_challenge_response

type: ``bool``

When enabled, authentication attempts will be interpreted as either the PIN or the answer to a challenge.
PIN concatenated with OTP can not be used anymore! Does only work when authenticating with a username.

.. _policy_force_challenge_response:

change_pin_via_validate
~~~~~~~~~~~~~~~~~~~~~~~

type: ``bool``

This works with the enrollment policies :ref:`policy_change_pin_first_use` and
:ref:`policy_change_pin_every`. When a PIN change is due, then a successful authentication
will start a challenge response mechanism in which the user is supposed to enter a new
PIN two times.

Only if the user successfully changes the PIN the authentication process is finished
successfully. E.g. if the user enters two different new PINs, the authentication process will fail.

.. note:: The application must support several consecutive challenge response requests.

.. _policy_resync_via_multichallenge:

resync_via_multichallenge
~~~~~~~~~~~~~~~~~~~~~~~~~

type: ``bool``

This policy is based on the global setting :ref:`autosync`.
If *AutoResync* is enabled and this policy is configured, a user can synchronize
their token during authentication via challenge response.

If privacyIDEA realizes that the first given OTP value is within the syncwindow,
a challenge will be presented to the user saying "To resync your token, please enter the next OTP value".
In contrast to the generic AutoResync a user has to enter the token PIN only once.

.. note:: The application must support several consecutive challenge response requests.

.. _policy_enroll_via_multichallenge:

enroll_via_multichallenge
~~~~~~~~~~~~~~~~~~~~~~~~~

type: ``string``

This policy allows the rollout of tokens during a successful authentication via `/validate/check`. A user could
authenticate via :ref:`passthru_policy` or using a registration code and right during this authentication session be
asked to enroll a new token.

The policy action can take one of the token types `hotp`, `totp`, `push`, `email`, `sms` or the container type
`smartphone`.

The clients and plugins should make use of this policy transparently and using multiple consecutive
challenges.

A new token is only enrolled if the user has no token of this type assigned yet. Additionally, the policies
:ref:`policy_max_token_per_user` and :ref:`policy_max_token_per_realm` are checked.

.. note:: During this kind of enrollment the policies for *require_description*
   and *verify_enrollment* are not checked.
   Also, currently no token PIN is set.

The different ways of enrollment are defined in detail by the token/container types:

**HOTP and TOTP**

If the policy is set to enroll an HOTP or a TOTP token, after successful authentication a QR code
is displayed to the user. The user has to scan the QR code and will then have to enter the valid OTP value,
generated by the newly scanned/enrolled token. Only after that, the user is finally authenticated.

The enrollment parameters, such as the hash algorithm or time step, are taken from the :ref:`token_config`. The user
policies :ref:`totp-timestep`, :ref:`hotp-hashlib` overwrite the default values from the token configuration.

.. note:: 2step enrollment is currently not supported in this enrollment scenario.

**SMS and Email**

After the first successful authentication step the user is presented with an input field to
enter their email address or mobile number. If done so, the user will then in the final step
have to enter the OTP value sent via email or text message.

.. note:: Enrolls an SMS token or Email token with the email address from the userstore
   can be easily accomplished with a *token event handler*. (See :ref:`event_token_enroll`).

**PUSH**

After the fist successful authentication step the user is presented a QR code for push token
enrollment. The user needs to scan the QR code with the privacyIDEA Authenticator App.
If the token is successfully enrolled, the user is logged in without any further interaction.
Since the successful enrollment of the Push token already verifies the presence of the user's smartphone,
there is no additional authentication step anymore during enrollment.

**Smartphone**

A smartphone container is only created if the user has no smartphone container assigned yet, and at least the
registration policy :ref:`container_policy_server_url` is defined.

After the first successful authentication step, the user is presented with a QR code for smartphone registration. The
user needs to scan the QR code with the privacyIDEA Authenticator App. If the container is registered successfully, the
user is logged in without any further interaction.

When using the :ref:`policy_enroll_via_multichallenge_template` policy, the container is created using the selected
template. This allows the container to be enrolled with multiple tokens at once. Note that for these tokens, all
enrollment policies are checked.


.. _policy_enroll_via_multichallenge_text:

enroll_via_multichallenge_text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

type: ``string``

There is a default text that is shown to the user, when a token or container is enrolled via multichallenge. The
administrator can change this text using this policy.


.. _policy_enroll_via_multichallenge_template:

enroll_via_multichallenge_template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

type: ``string``

Select a container template for the smartphone container that is used during enrollment via multichallenge. This means
you can enroll a container and multiple tokens at once. For the tokens, all enrollment policies are checked. If an
error occurs during the enrollment of a token, it fails silently, and the remaining tokens can still be enrolled.

If this policy contains an invalid template name, the container is enrolled anyway, but without a template.

The policy :ref:`policy_enroll_via_multichallenge` has to be set to `smartphone` for this policy to take effect.


.. _policy_u2f_facets:

u2f_facets
~~~~~~~~~~

type: ``string``

This is a white space separated list of domain names, that are trusted to
also use a U2F device that was registered with privacyIDEA.

You need to specify a list of FQDNs without the https scheme like:

*"host1.example.com host2.example.com firewall.example.com"*

For more information on configuring U2F see :ref:`u2f_token`.


.. [#pythonre] https://docs.python.org/3/library/re.html

.. _reset_all_user_tokens:

reset_all_user_tokens
~~~~~~~~~~~~~~~~~~~~~

type: ``bool``

If a user authenticates successfully all failcounter of all of their tokens
will be reset. This can be important, if using empty PINs or *otppin=None*.

increase_failcounter_on_challenge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

type: ``bool``

The normal behaviour is: to not increase the failcounter in case of challenge response.

If this policy is activated the failcounter is increased for each token for which a challenge
is triggered.

The reason for this is that an attack can no longer trigger an infinite number
of SMS or emails, for example. Because once the maximum failcounter has been reached,
no further challenges for these tokens can be triggered.

.. note:: It should be noted that for all tokens for which a challenge has been generated,
   the failcounter will be incremented. In the case of validate/triggerchallenge, the failcounters are increased for all tokens.
   In some cases it makes sense to use this policy together with :ref:`reset_all_user_tokens`.

.. _policy_auth_cache:

auth_cache
~~~~~~~~~~

.. index:: AuthCache, Authentication Cache

type: ``string``

The Authentication Cache caches the credentials of a successful authentication
and allows using the same credentials (inluding the OTP value) for the specified
amount of time and optionally for a specified number of authentications.

The time to cache the credentials can be specified like "4h", "5m", "2d", "3s"
(hours, minutes, days, seconds). The number of allowed authentications can be
specified as a whole number, greater than zero.

The notation "4h/5m" means that credentials
are cached for 4 hours, but may only be used again, if every 5 minutes the
authentication occurs. If the authentication with the same credentials would
not occur within 5 minutes, the credentials can not be used anymore.

The notation "2m/3" means that credentials are cached for 2 minutes, but may only be used 3 times
in this timeframe.

In future implementations the caching of the credentials could also be
dependent on the clients IP address and the user agent.

.. note:: Cache entries are written to the database table ``authcache``. Please note
   that expired entries are automatically deleted only when the user
   attempts to log in with the same expired credentials again. In all other cases,
   expired entries need to be deleted from this table manually by running::

      pi-manage config authcache cleanup --minutes MIN

   which deletes all cache entries whose last authentication has occurred at least
   ``MIN`` minutes ago. As an example::

      pi-manage config authcache cleanup --minutes 300

   will delete all authentication cache entries whose last authentication happened more
   than 5 hours ago.

   It may make sense to create a cronjob that periodically cleans up old authentication cache entries.

.. note:: The AuthCache only works for user authentication, not for
   authentication with serials.

.. _policy_push_text_on_mobile:

push_text_on_mobile
~~~~~~~~~~~~~~~~~~~

.. index:: push token, Firebase service

type: ``string``

This is the text that should be displayed on the push notification
during the login process with a :ref:`push_token`.
You can choose different texts for different users or IP addresses.
This way you could customize push notifications for different applications.

You can also use certain tags in the text, just like in :ref:`emailtext`.

.. _policy_push_title_on_mobile:

push_title_on_mobile
~~~~~~~~~~~~~~~~~~~~

.. index:: push token, Firebase service

type: ``string``

This is the title of the push notification that is displayed
on the user's smartphone during the login process with
a :ref:`push_token`.

.. _policy_push_wait:

push_wait
~~~~~~~~~

.. index:: push token, push direct authentication

type: ``integer``

This can be set to a number of seconds. If this is set, the authentication
with a push token is only performed via one request to ``/validate/check``.
The HTTP request to ``/validate/check`` will wait up to this number of
seconds and check, if the push challenge was confirmed by the user.

This way push tokens can be used with any non-push-capable applications.

Sensible numbers might be 10 or 20 seconds.

.. note:: This behaviour can interfere with other tokentypes. Even if
   the user also has a normal HOTP token, the ``/validate/check`` request
   will only return after this number of seconds.

.. warning:: Using simple webserver setups like Apache WSGI this actually
   can block all available worker threads, which will cause privacyIDEA
   to become unresponsive if the number of open PUSH challenges exceeds
   the number of available worker threads!

.. _policy_push_require_presence:

push_require_presence
~~~~~~~~~~~~~~~~~~~~~

.. index:: push token

type: ``bool``

If this policy is set, the login window will display a message like
``Please confirm login by pressing Button 'C' on your smartphone``.

The push notification on the smartphone will show several buttons. One is labeled ``C``.

The user then can confirm the login by pressing this button. All other buttons will decline the
login request.

.. note:: This mechanism allows login scenarios where the user in front of the login window and the
   person owning the smartphone are two different persons. In this case they will have to communicate
   for a successful login.

If this policy is not set, the PUSH message will simply ask the user if they
want to log in.

.. versionadded:: 3.10

.. _policy_push_presence_options:

push_presence_options
~~~~~~~~~~~~~~~~~~~~~

.. index:: push token

type: ``string``

Takes only effect if :ref:`policy_push_require_presence` is set.

This policy configures the buttons that are displayed in the push notification on the smartphone.

The following options are available:

``ALPHABETIC``

    The buttons are labeled with the letters A to Z.

``NUMERIC``

    The buttons are labeled with the numbers 01 to 99.

``CUSTOM``

    The buttons are labeled with the characters defined in the policy :ref:`policy_push_presence_custom_options`.
    If the :ref:`policy_push_presence_custom_options` policy is not set, the fallback is to use the ``ALPHABETIC`` options.

The default is to use the ``ALPHABETIC`` options.

.. versionadded:: 3.10

.. _policy_push_presence_custom_options:

push_presence_custom_options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: push token

type: ``string``

Takes only effect if :ref:`policy_push_presence_options` is set to ``CUSTOM``.

This policy configures the buttons that can be displayed in the push notification on the smartphone.
To set the number of buttons, see :ref:`push_presence_num_options`.

The string must contain at least 2 options and should be unique.

The options are separated by ":" e.g. ``01:02:03:1A:1B:1C``

.. versionadded:: 3.10

.. _push_presence_num_options:

push_presence_num_options
~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: push token

type: ``integer``

Takes only effect if :ref:`policy_push_require_presence` is set.

This policy configures the number of buttons that are displayed in the push notification on the smartphone.
The default is 3 buttons. If the configured number of buttons is not possible, it will be clamped to the next possible value.

.. versionadded:: 3.10

.. _policy_auth_push_allow_poll:

push_allow_polling
~~~~~~~~~~~~~~~~~~

.. index:: push token

type: ``string``

This policy configures if push tokens are allowed to poll the server for open
challenges (e.g. when the third-party push service is unavailable or
unreliable).

The following options are available:

``allow``

    *Allow* push tokens to poll for challenges.

``deny``

    *Deny* push tokens to poll for challenges. This basically returns a ``403``
    error when requesting the poll endpoint.

``token``

    *Allow* / *Deny* polling based on the individual token. The tokeninfo key
    ``polling_allowed`` is checked. If the value evaluates to ``False``, polling
    is denied for this token. If it evaluates to ``True`` or is not set, polling
    is allowed for this token.

The default is to ``allow`` polling

.. _policy_push_ssl_verify_auth:

push_ssl_verify
~~~~~~~~~~~~~~~

type: ``integer``

The smartphone needs to verify the SSL certificate of the privacyIDEA server during
the authentication with push tokens. By default, the verification is enabled. To disable
verification during enrollment, see :ref:`policy_push_ssl_verify_enrollment`.

.. _policy_challenge_text:
.. _challenge-text:
.. _challenge-text-footer:
.. _challenge-text-header:

challenge_text, challenge_text_header, challenge_text_footer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. index:: Challenge Text Policy

Using these policies the administrator can modify the challenge texts
of e.g. the Email- or SMS-Token. The action *challenge_text* changes the
challenge text in general, no matter which challenge response token is used.

If the *challenge_text_header* is set and if there are more matching
challenge response tokens, then the texts of all tokens are
concatenated together. Double challenge texts are reduced to one text only.

The *challenge_text_header* and *challenge_text_footer* may contain HTML.
If the *challenge_text_header* ends with an ``<ul>`` or ``<ol>``, then
all the challenge texts are formatted as an ordered or unordered list.
In this case the *challenge_text_footer* also should contain the closing
tag.

.. note:: The footer will only be used, if the header is also set.

.. note:: Starting with version 3.11 the `challenge-text` can contain tags similar to the
    policy :ref:`emailtext`:

    * {serial} the serial number of the token.
    * {user} the given name of the token owner.
    * {givenname} the given name of the token owner.
    * {surname} the surname of the token owner.
    * {username} the loginname of the token owner.
    * {userrealm} the realm of the token owner.
    * {tokentype} the type of the token.
    * {time} the current server time in the format HH:MM:SS.
    * {date} the current server date in the format YYYY-MM-DD.
    * {phone} the phone number from the challenge in case of sms token.
    * {email} email address from the challenge in case of email token.
    * {presence_answer} only for push token and only if require_presence is enabled.

.. _policy_indexedsecret:

indexedsecret_challenge_text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Indexed Secret Token asks the user to provide the characters of the
secret from certain positions. The default text is:

*Please enter the position 3,1,6,7 from your secret.*

with *3,1,6,7* being the positions of the characters, the user is supposed to
enter. This text can be changed with this policy setting.
The text needs to contain the python formatting tag *{0!s}* which will
be replaced with the list of the requested positions.

For more details of this token type see :ref:`indexedsecret_token`.


.. _policy_webauthn_challenge_text_auth:

webauthn_challenge_text
~~~~~~~~~~~~~~~~~~~~~~~

type: ``string``

Use an alternate challenge text for requesting the user to confirm with
their WebAuthn token during authentication. This might be different from the
challenge text received during enrollment
(see :ref:`policy_webauthn_challenge_text_enrollment`).


.. _email-challenge-text:
.. _sms-challenge-text:
.. _u2f-challenge-text:

email_challenge_text, sms_challenge_text, u2f_challenge_text
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

type: ``string``

With these actions the administrator may set alternative challenge texts for email, SMS
and U2F tokens.


indexedsecret_count
~~~~~~~~~~~~~~~~~~~

The Indexed Secret Token asks the used for a number of characters from
a shared secret. The default number to ask is 2.

The number of requested positions can be changed using this policy.


.. _policy_webauthn_authn_allowed_transports:

webauthn_allowed_transports
~~~~~~~~~~~~~~~~~~~~~~~~~~~

type: ``string``

This action determines which transports may be used to communicate with the
authenticator during authentication. For instance, if the authenticators used
support both a USB connection and NFC wireless communication, they can be
limited to USB only using this policy. The allowed transports are declared as a
space-separated list.

The default is to allow all transports (equivalent to a value of `usb ble nfc
internal`).

.. _policy_webauthn_authn_timeout:

webauthn_timeout
~~~~~~~~~~~~~~~~

type: ``integer``

This action sets the time in seconds the user has to confirm an authentication
request on their WebAuthn authenticator.

This is a client-side setting, that governs how long the client waits for the
authenticator. It is independent of the time for which a challenge for a
challenge response token is valid, which is governed by the server and
controlled by a separate setting. This means, that if you want to increase this
timeout beyond two minutes, you will have to also increase the challenge
validity time, as documented in :ref:`challenge_validity_time`.

This setting is a hint. It is interpreted by the client and may be adjusted by
an arbitrary amount in either direction, or even ignored entirely.

The default timeout is 60 seconds.

.. note:: If you set this policy you may also want to set
    :ref:`policy_webauthn_enroll_timeout`.

.. _policy_webauthn_authn_user_verification_requirement:

webauthn_user_verification_requirement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

type: ``string``

This action configures whether the user's identity should be checked when
authenticating with a WebAuthn token. If this is set to required, any user
signing in with their WebAuthn token will have to provide some form of
verification. This might be biometric identification or knowledge-based,
depending on the authenticator used.

This defaults to `preferred`, meaning user verification will be performed if
supported by the token.

.. note:: User verification is different from user presence checking. The
    presence of a user will always be confirmed (by asking the user to take
    action on the token, which is usually done by tapping a button on the
    authenticator). User verification goes beyond this by ascertaining that the
    user is indeed the same user each time (for example through biometric
    means). Only set this to `required` if you know for a fact, that you have
    authenticators, that actually support some form of user verification (these
    are still quite rare in practice).

.. note:: If you configure this, you will likely also want to configure
    :ref:`policy_webauthn_enroll_user_verification_requirement`.


question_number
~~~~~~~~~~~~~~~

type: ``integer``

The questionnaire token can ask more than one question during one authentication process.
It will ask the first question, verify the answer, ask the next question and verify the answer.
This policy setting defines how many questions the user needs to answer.

The default amount to ask is 1.

.. note:: A question will be asked only once, unless the policy requires more questions to be asked,
   than the token has available answers.

preferred_client_mode
~~~~~~~~~~~~~~~~~~~~~

type: ``string``

This action sets a list of the client mode in the preferred order. You can enter the different client
modes in the order you like. For example: "interactive webauthn poll u2f". The client you are using
will show you the correct login for your preferred client mode. For example if this is your list:
"interactive webauthn poll u2f" and in your multi-challenge list are a webauthn and u2f token,
then your client will automatically show you the login for a webauthn token.

The default list is "interactive webauthn poll u2f".

client_mode_per_user
~~~~~~~~~~~~~~~~~~~~

type: ``bool``

If this policy is set, the token type recently used during a successful authentication is stored per user and
application. For the next authentication, the last used token type is used to identify the preferred client mode. The
client you are using will show the correct login for the user's preferred client mode. For example, if the user lastly
used a TOTP token to authenticate, an input field to enter the OTP value is displayed.

This policy takes precedence over the `preferred_client_mode` policy.

passkey_trigger_by_pin
~~~~~~~~~~~~~~~~~~~~~~

type: ``bool``

If this policy is set, the passkey token can be triggered with its PIN or via the /validate/triggerchallenge endpoint.
For privacyIDEA plugins, enabling this is not recommended. It is advised to use a condition with this policy,
for example on the user-agent.
