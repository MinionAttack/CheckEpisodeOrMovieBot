# -*- coding: utf-8 -*-

START_COMMAND_TEXT = f"Use this command to see the welcome message.\n"

STATUS_COMMAND_TEXT = f"Use this command to check if the bot is up and running. <strong>If you do not get a response from this command," \
                      f" the bot is not working</strong>.\n"

OPTIONS_COMMAND_TEXT = f"Use this command to read the text you are reading (hehe).\n"

FIND_COMMAND_TEXT = f"Use this command to find a specific episode of a TV Show. There are two types of syntax, one short and one long.\n" \
                    f"\nTo use the long syntax you must write: /find -tv_show name -season number -episode number -quality number\n" \
                    f"\nTo use the short syntax you must write: /find -ts name -s number -e number -q number\n\n<strong>Important notes:" \
                    f"</strong>\n\n1. The name of the TV show must be spelled the same way it is displayed on <strong>IMDb</strong>.\n2. " \
                    f"The number specified for the quality must not include the scan type. If you want HD content write 720 but not 720i " \
                    f"or 720p, the same for Full HD (1080) content and Ultra HD content (4K). <strong>Do not include the letter</strong>."
