import os
import json
from typing import Tuple, List, Dict, Any
from .reasoning_engine import ReasoningEngine, ReasoningStep, ChainOfThought


class OllamaEngine:
    def __init__(self, model_name: str = "llama3"):
        self.model_name = model_name
        self.client = None
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self._initialize_client()

    def _initialize_client(self):
        try:
            import requests
            self.client = requests
            # Testear conexión
            response = self.client.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                print(f"✅ Conexión a Ollama exitosa! Modelos disponibles: {[m['name'] for m in response.json()['models']]}")
            else:
                print(f"⚠️ Ollama respondió pero hubo un problema")
        except Exception as e:
            print(f"⚠️ No se pudo conectar a Ollama: {e}")
            self.client = None
        except ImportError:
            print("⚠️ No hay un problema con las dependencias")

    def _call_ollama(self, prompt: str, system_prompt: str = None) -> str:
        if not self.client:
            raise Exception("Ollama no está disponible, usando razonamiento básico")
        
        system_msg = "Eres Kofu, un asistente de IA para crear documentos y presentaciones. Responde de forma clara y útil."
        
        if system_prompt:
            system_msg = system_prompt
        
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "temperature": 0.7
        }
        
        try:
            response = self.client.post(f"{self.base_url}/api/chat", json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except Exception as e:
            raise Exception(f"Error al comunicarse con Ollama: {e}")


class HybridReasoningEngine(ReasoningEngine):
    def __init__(self, use_ollama: bool = True):
        super().__init__()
        self.ollama_engine = OllamaEngine() if use_ollama else None

    def reason(self, user_input: str) -> Tuple[str, List[ReasoningStep]]:
        self.thinking_steps = []
        self.clear_facts()
        self.add_fact(user_input)
        
        self.thinking_steps.append(ReasoningStep(1, "Analizando entrada del usuario", user_input))
        
        topic = self._extract_topic(user_input)
        if topic:
            self.thinking_steps.append(ReasoningStep(2, f"Tema identificado: {topic}"))
        
        try:
            if self.ollama_engine and self.ollama_engine.client:
                self.thinking_steps.append(ReasoningStep(3, "Usando IA de razonamiento avanzado (Ollama)", "Modelo: llama3"))
                response = self.ollama_engine._call_ollama(user_input)
                self.thinking_steps.append(ReasoningStep(4, "Generando respuesta final"))
                return response, self.thinking_steps
            else:
                self.thinking_steps.append(ReasoningStep(3, "Ollama no disponible, usando razonamiento básico"))
                return super().reason(user_input)
        except Exception as e:
            self.thinking_steps.append(ReasoningStep(3, f"Error con Ollama, usando razonamiento básico", str(e)))
            return super().reason(user_input)
