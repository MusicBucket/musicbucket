from django import views


class TelegramLoginCallbackView(views.View):
    """
    DEPRECATED
    Telegram Login Callback View.
    When a user confirms the Telegram Login, it will be redirected to this view.
    This view is the responsible lo create Profile/User and Link it to the existent (or not) TelegramUser
    request.GET = QueryDict: {'id': ['80461220'], 'first_name': ['Pau'], 'username': ['pauriera'],
                  'photo_url': ['https://t.me/i/userpic/320/9GH17T011HkzD0ElT9YeCJh_4nh_p9iSCOpGz1qvShU.jpg'],
                  'auth_date': ['1585908195'],
                  'hash': ['78707e83eff02a767008ffcf1611656f37f4ce60f57c7e8f4956491687a8da57']} >
    """
    pass
    # def get(self, request, *args, **kwargs):
    #     try:
    #         telegram_auth_result = verify_telegram_authentication(
    #             bot_token=settings.TELEGRAM_BOT_TOKEN, request_data=request.GET
    #         )
    #     except TelegramDataIsOutdatedError:
    #         return HttpResponse(_("Outdated Telegram authentication data"))
    #     except NotTelegramDataError:
    #         return HttpResponse(_("Received data has nothing to do with Telegram"))
    #
    #     user = self._link_telegram_user_to_a_new_user_profile(telegram_auth_result)
    #     if user:
    #         login(request, user)
    #         messages.info(request, _("Login successful"))
    #     else:
    #         messages.error(request, _("Error login in with Telegram"))
    #     return redirect("web:home")
    #
    # @staticmethod
    # def _link_telegram_user_to_a_new_user_profile(telegram_auth_result):
    #     telegram_user, _ = TelegramUser.objects.update_or_create(
    #         telegram_id=telegram_auth_result.get("id"),
    #         defaults={
    #             "username": telegram_auth_result.get("username", ""),
    #             "first_name": telegram_auth_result.get("first_name", ""),
    #             "photo_url": telegram_auth_result.get("photo_url", ""),
    #         },
    #     )
    #     profile = telegram_user.profile
    #     if not profile:
    #         user_model = get_user_model()
    #         generated_password = user_model.objects.make_random_password()
    #         user, _ = user_model.objects.get_or_create(
    #             username=telegram_user.username,
    #             defaults={"password": generated_password},
    #         )
    #         profile, _ = Profile.objects.get_or_create(user_id=user.pk)
    #         telegram_user.profile = profile
    #         telegram_user.save(update_fields=["profile"])
    #         return user
    #     return profile.user
