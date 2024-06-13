import unittest
from unittest.mock import patch
from automatizacion_consultas import fetch_data 

class TestFetchData(unittest.TestCase):
    def setUp(self):
        self.page = 1
        self.size = 1000
        self.document = "0968599020001"
        self.type_process = "actor"

    @patch('requests.post')
    def test_fetch_data_success(self, mock_post):
        # Configura el mock para simular una respuesta exitosa
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "data": "Some data"}

        # Llama a la función con los valores mockeados
        response = fetch_data(self.page, self.size, self.document, self.type_process)
        
        # Verifica que la respuesta es como se esperaba
        self.assertEqual(response, {"success": True, "data": "Some data"})
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_fetch_data_failure(self, mock_post):
        # Configura el mock para simular una respuesta fallida
        mock_response = mock_post.return_value
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Bad request"}

        # Llama a la función
        response = fetch_data(self.page, self.size, self.document, self.type_process)
        
        # Verifica que la función maneja correctamente el error
        self.assertIsNone(response)
        self.assertEqual(mock_post.call_count, 1)

if __name__ == '__main__':
    unittest.main()