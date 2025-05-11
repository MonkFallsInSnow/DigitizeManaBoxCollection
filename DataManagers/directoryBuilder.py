import logging
import re
from pathlib import Path
from Constants.argumentOptions import OrganizationOptions
from Constants.colors import ColorIdentity


class DirectoryBuilder:
    def __init__(self, output_dir_str, collection_root_name="MTG_Collection"):
        """
        Initializes the DirectoryBuilder.

        Args:
            output_dir_str: The string path to the base output directory where the
                            collection root folder will be created.
            collection_root_name: The name of the root directory for the MTG collection.
                                 Defaults to "MTG_Collection".
        """
        self._output_dir = Path(output_dir_str)
        self._root_dir = self._output_dir / collection_root_name
        self._folder_char_map = {
            ord(':'): None, ord('<'): None, ord('>'): None, ord('"'): None,
            ord('/'): '-', ord('\\'): None, ord('|'): None, ord('?'): None, ord('*'): None,
        }  # For str.translate to remove/replace forbidden chars

    def _sanitize_name(self, name):
        """
        Sanitizes a string to be used as a valid file or directory name.
        Removes or replaces characters that are invalid in most filesystems.

        Args:
            name: The string to sanitize.

        Returns:
            A sanitized version of the name.
        """
        if not name:
            return ""

        # Handle Scryfall's typical " // " in names like "Wear // Tear"
        name = name.replace(' // ', ' - ')

        # Remove/replace forbidden characters
        sanitized = name.translate(self._folder_char_map)

        # Remove leading/trailing whitespace and dots (problematic on Windows)
        sanitized = sanitized.strip(" .")

        # Replace multiple spaces with a single space
        sanitized = re.sub(r'\s+', ' ', sanitized)

        if not sanitized:
            return "_empty_name_"

        return sanitized

    def build_directories(self, card_collection, organization_options):
        """
        Builds the directory structure and saves card images.

        Args:
            card_collection: The CardCollection object containing all card data.
            organization_options: A list of strings representing the chosen organization
                                  criteria (e.g., ['color', 'type', 'rarity']).
        """
        logging.info(f"Building directory structure in: {self._root_dir}")
        try:
            self._root_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            logging.error(f"Could not create root directory {self._root_dir}: {e}")
            return

        sorted_cards = sorted(card_collection.cards.values(), key=lambda card: card.name)

        for card in sorted_cards:
            path_segments_for_card = []

            for option_key_str in organization_options:
                current_segments_for_option = []

                if option_key_str == OrganizationOptions.COLOR.value:
                    colors = card.color_identity
                    verbose_color_list = ColorIdentity.to_value_list(colors)

                    if len(verbose_color_list) == 1:
                        current_segments_for_option.append(verbose_color_list[0])
                    else:
                        current_segments_for_option.append("Multicolor")
                        current_segments_for_option.append(ColorIdentity.to_verbose_color_identity(colors))

                elif option_key_str == OrganizationOptions.TYPE.value:
                    if card.card_types and card.card_types.type_data and card.card_types.type_data.front_face_types:
                        raw_type = card.card_types.type_data.front_face_types[0]
                        current_segments_for_option.append(raw_type.capitalize())
                    else:
                        current_segments_for_option.append("UnknownType")

                elif option_key_str == OrganizationOptions.SET.value:
                    set_val = card.set_name
                    current_segments_for_option.append(set_val if set_val else "UnknownSet")

                elif option_key_str == OrganizationOptions.RARITY.value:
                    rarity_val = card.rarity
                    current_segments_for_option.append(rarity_val.capitalize() if rarity_val else "UnknownRarity")

                for segment in current_segments_for_option:
                    sanitized_segment = self._sanitize_name(segment)
                    if sanitized_segment:
                        path_segments_for_card.append(sanitized_segment)

            current_card_path = self._root_dir
            for segment_name in path_segments_for_card:
                current_card_path /= segment_name

            try:
                current_card_path.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                logging.error(f"Could not create directory {current_card_path} for card {card.name}: {e}")
                continue

            sanitized_card_name = self._sanitize_name(card.name)

            if not sanitized_card_name:
                logging.warning(f"Card name '{card.name}' sanitized to an empty string. Skipping.")
                continue

            if card.has_multiple_faces and card.back_image:
                card_specific_folder_name = f"{sanitized_card_name}({card.quantity})"
                card_folder_path = current_card_path / card_specific_folder_name

                try:
                    card_folder_path.mkdir(parents=True, exist_ok=True)
                except OSError as e:
                    logging.error(f"Could not create card-specific folder {card_folder_path} for {card.name}: {e}")
                    continue

                # Image Naming Note (as before):
                # This uses "<CardName>_front.jpg" and "<CardName>_back.jpg". For distinct face names
                # (e.g., "Front_Face_Name.jpg"), Card class and ScryfallAPI updates are needed.
                front_image_filename = self._sanitize_name(f"{sanitized_card_name}_front.jpg")
                back_image_filename = self._sanitize_name(f"{sanitized_card_name}_back.jpg")

                if card.front_image:
                    try:
                        with open(card_folder_path / front_image_filename, 'wb') as f:
                            f.write(card.front_image)
                    except OSError as e:
                        logging.error(
                            f"Error writing front image for {card.name} to {card_folder_path / front_image_filename}: {e}")
                else:
                    logging.warning(
                        f"Missing front image data for multi-face card: {card.name} (Scryfall ID: {card.scryfall_id})")

                if card.back_image:
                    try:
                        with open(card_folder_path / back_image_filename, 'wb') as f:
                            f.write(card.back_image)
                    except OSError as e:
                        logging.error(
                            f"Error writing back image for {card.name} to {card_folder_path / back_image_filename}: {e}")

            else:
                card_file_name = f"{sanitized_card_name}({card.quantity}).jpg"
                if card.front_image:
                    try:
                        with open(current_card_path / card_file_name, 'wb') as f:
                            f.write(card.front_image)
                    except OSError as e:
                        logging.error(
                            f"Error writing image for {card.name} to {current_card_path / card_file_name}: {e}")
                else:
                    logging.warning(f"Missing image data for card: {card.name} (Scryfall ID: {card.scryfall_id})")

        logging.info("Directory structure and card image saving process completed.")