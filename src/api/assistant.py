from typing import Dict, Optional, Tuple
import re
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.design_generator import DesignGenerator
from models.render_generator import RenderGenerator


class MultimodalAssistant:
    def __init__(self):
        self.design_generator = DesignGenerator()
        self.render_generator = None
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        return """Eres un asistente de diseno arquitectonico multimodal.
Puedes generar especificaciones tecnicas y renderizados fotorrealistas.
Analiza la solicitud del usuario y determina si necesita texto, imagen, o ambos."""

    def _parse_user_intent(self, user_message: str, config: Dict) -> Dict:
        message_lower = user_message.lower()

        intent = {
            "generate_spec": False,
            "generate_image": False,
            "style": config.get("style", "modern"),
            "space": None,
            "size": "medium",
            "colors": [],
        }

        image_keywords = [
            "render",
            "imagen",
            "foto",
            "visualizar",
            "mostrar",
            "generar imagen",
        ]
        spec_keywords = [
            "especificacion",
            "detalles",
            "materiales",
            "presupuesto",
            "tecnico",
        ]

        intent["generate_image"] = any(kw in message_lower for kw in image_keywords)
        intent["generate_spec"] = any(kw in message_lower for kw in spec_keywords)

        if not intent["generate_image"] and not intent["generate_spec"]:
            if config.get("default_mode") == "auto":
                intent["generate_spec"] = True
                intent["generate_image"] = True
            elif config.get("default_mode") == "spec":
                intent["generate_spec"] = True
            elif config.get("default_mode") == "image":
                intent["generate_image"] = True

        styles = [
            "rustic",
            "brutalism",
            "minimalist",
            "industrial",
            "modern",
            "mediterranean",
            "scandinavian",
            "contemporary_luxury",
        ]
        for style in styles:
            if style in message_lower or style.replace("_", " ") in message_lower:
                intent["style"] = style
                break

        spaces = [
            "facade",
            "living_room",
            "kitchen",
            "bathroom",
            "bedroom",
            "office",
            "restaurant",
            "store",
        ]
        space_map = {
            "fachada": "facade",
            "sala": "living_room",
            "cocina": "kitchen",
            "bano": "bathroom",
            "dormitorio": "bedroom",
            "oficina": "office",
            "restaurante": "restaurant",
            "tienda": "store",
        }

        for space in spaces:
            if space in message_lower or space.replace("_", " ") in message_lower:
                intent["space"] = space
                break

        for es_space, en_space in space_map.items():
            if es_space in message_lower:
                intent["space"] = en_space
                break

        if "pequeno" in message_lower or "small" in message_lower:
            intent["size"] = "small"
        elif "grande" in message_lower or "large" in message_lower:
            intent["size"] = "large"

        color_keywords = [
            "gris",
            "grey",
            "gray",
            "beige",
            "blanco",
            "white",
            "negro",
            "black",
            "madera",
            "wood",
            "terracota",
            "terracotta",
        ]
        for color in color_keywords:
            if color in message_lower:
                intent["colors"].append(color)

        return intent

    def process_request(self, user_message: str, config: Dict) -> Dict:
        intent = self._parse_user_intent(user_message, config)

        if not intent["space"]:
            return {
                "type": "text",
                "content": "Por favor especifica el tipo de espacio (fachada, sala, cocina, etc.)",
                "metadata": {},
            }

        response = {
            "type": "multimodal",
            "text_content": None,
            "image_path": None,
            "metadata": intent,
        }

        if intent["generate_spec"]:
            specification = self.design_generator.generate_specification(
                style=intent["style"],
                space=intent["space"],
                size=intent["size"],
                colors=intent["colors"],
            )
            response["text_content"] = specification

        if intent["generate_image"]:
            if self.render_generator is None:
                self.render_generator = RenderGenerator()

            spec_for_render = response["text_content"] or "Architectural design"

            output_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "outputs/renders"
            )

            filename = f"{intent['style']}_{intent['space']}_{intent['size']}.png"

            _, image_path = self.render_generator.generate_render(
                style=intent["style"],
                space=intent["space"],
                specification=spec_for_render,
                colors=intent["colors"],
                output_dir=output_dir,
                filename=filename,
                num_inference_steps=config.get("max_steps", 50),
                guidance_scale=config.get("guidance_scale", 7.5),
            )

            response["image_path"] = image_path

        return response

    def get_available_options(self) -> Dict:
        return self.design_generator.get_available_options()
