# -*- coding: utf-8 -*-

INCORRECT_FORMAT_HELP = f"Incorrect format, see the /help command for more details. \U0001F635"

START_COMMAND_TEXT = f"Use this command to see the welcome message. \U0001F44B"

STATUS_COMMAND_TEXT = f"Use this command to check if the bot is up and running. <strong>If you do not get a response from this command," \
                      f" the bot is not working</strong>. \U0001F6A5"

HELP_COMMAND_TEXT = f"Use this command to know how to use the bot. There are two types of syntax, one short and one long.\n\nTo use the " \
                    f"long syntax you must write:\n/help -command command\n\nTo use the short syntax you must write:\n/help -c command\n" \
                    f"\n<strong>Available commands:</strong>\n\n1. start\n2. status\n3. help\n4. series\n5. movies"

SERIES_COMMAND_TEXT = f"Use this command to find a specific episode of a series. There are two types of syntax, one short and one long." \
                      f"\n\nTo use the long syntax you must write:\n/series -name name -season number -episode number -quality number\n" \
                      f"\nTo use the short syntax you must write:\n/series -n name -s number -e number -q number\n\n<strong>Important " \
                      f"notes:</strong>\n\n1. The name of the series must be spelled the same way it is displayed on <strong>IMDb" \
                      f"</strong>.\n2. The available qualities are: 480 (SD), 720 (HD), 1080 (FHD) and 2160 (UHD).\n3. The number " \
                      f"specified for the quality must not include the scan type. If you want HD content write 720 but not 720i or 720p, " \
                      f"the same for SD (480) content, Full HD (1080) content and Ultra HD (2160) content. <strong>Do not include the " \
                      f"letter</strong>."

MOVIES_COMMAND_TEXT = f"Use this command to find a specific movie. There are two types of syntax, one short and one long.\n\nTo use the" \
                      f"long syntax you must write:\n/movies -name name -quality number\n\nTo use the short syntax you must write:\n" \
                      f"/movies -n name -q number\n\n<strong>Important notes:</strong>\n\n1. The name of the movie must be spelled the " \
                      f"same way it is displayed on <strong>IMDb</strong>.\n2. The available qualities are: 480 (SD), 720 (HD), 1080 " \
                      f"(FHD) and 2160 (UHD).\n3. The number specified for the quality must not include the scan type. If you want HD " \
                      f"content write 720 but not 720i or 720p, the same for SD (480) content, Full HD (1080) content and Ultra HD " \
                      f"(2160) content. <strong>Do not include the letter</strong>."
