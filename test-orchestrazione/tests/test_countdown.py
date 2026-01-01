#!/usr/bin/env python3
"""
Test Suite: Countdown Feature
Testa la logica di countdown per eventi con date future, presenti e passate.
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime, date

# Aggiungi path del modulo da testare
sys.path.insert(0, str(Path(__file__).parent.parent / "api"))

from countdown import get_countdown, handle_request


class TestCountdownLogic(unittest.TestCase):
    """Test della logica di countdown basata su date."""

    def _mock_today(self, year, month, day):
        """Helper per moccare date.today() con una data specifica."""
        mock_date = MagicMock()
        mock_date.today.return_value = date(year, month, day)
        return mock_date

    @patch('countdown.date')
    def test_data_futura_un_giorno(self, mock_date):
        """Test: Data domani → 1 giorno rimanente."""
        mock_date.today.return_value = date(2026, 1, 1)

        result = get_countdown("2026-01-02", "Evento Domani")

        self.assertEqual(result["days_remaining"], 1)
        self.assertEqual(result["target_date"], "2026-01-02")
        self.assertEqual(result["event_name"], "Evento Domani")
        self.assertFalse(result["is_past"])
        self.assertFalse(result["is_today"])

    @patch('countdown.date')
    def test_data_futura_una_settimana(self, mock_date):
        """Test: Data tra 7 giorni → 7 giorni rimanenti."""
        mock_date.today.return_value = date(2026, 1, 1)

        result = get_countdown("2026-01-08")

        self.assertEqual(result["days_remaining"], 7)
        self.assertEqual(result["target_date"], "2026-01-08")
        self.assertEqual(result["event_name"], "Evento")  # Default
        self.assertFalse(result["is_past"])
        self.assertFalse(result["is_today"])

    @patch('countdown.date')
    def test_data_futura_un_anno(self, mock_date):
        """Test: Data tra 365 giorni → 365 giorni rimanenti."""
        mock_date.today.return_value = date(2026, 1, 1)

        result = get_countdown("2027-01-01", "Capodanno 2027")

        self.assertEqual(result["days_remaining"], 365)
        self.assertEqual(result["event_name"], "Capodanno 2027")
        self.assertFalse(result["is_past"])
        self.assertFalse(result["is_today"])

    @patch('countdown.date')
    def test_data_oggi(self, mock_date):
        """Test: Data oggi → 0 giorni rimanenti, is_today = True."""
        mock_date.today.return_value = date(2026, 1, 1)

        result = get_countdown("2026-01-01", "Oggi!")

        self.assertEqual(result["days_remaining"], 0)
        self.assertTrue(result["is_today"])
        self.assertFalse(result["is_past"])

    @patch('countdown.date')
    def test_data_passata_un_giorno(self, mock_date):
        """Test: Data ieri → -1 giorno, is_past = True."""
        mock_date.today.return_value = date(2026, 1, 2)

        result = get_countdown("2026-01-01", "Evento Passato")

        self.assertEqual(result["days_remaining"], -1)
        self.assertTrue(result["is_past"])
        self.assertFalse(result["is_today"])

    @patch('countdown.date')
    def test_data_passata_un_mese(self, mock_date):
        """Test: Data 30 giorni fa → -30 giorni."""
        mock_date.today.return_value = date(2026, 2, 1)

        result = get_countdown("2026-01-02", "Evento Gennaio")

        self.assertEqual(result["days_remaining"], -30)
        self.assertTrue(result["is_past"])
        self.assertFalse(result["is_today"])

    @patch('countdown.date')
    def test_event_name_default(self, mock_date):
        """Test: Event name default quando non specificato."""
        mock_date.today.return_value = date(2026, 1, 1)

        result = get_countdown("2026-12-31")

        self.assertEqual(result["event_name"], "Evento")

    @patch('countdown.date')
    def test_event_name_custom(self, mock_date):
        """Test: Event name custom viene usato correttamente."""
        mock_date.today.return_value = date(2026, 1, 1)

        result = get_countdown("2026-12-25", "Natale 2026")

        self.assertEqual(result["event_name"], "Natale 2026")


class TestHandleRequest(unittest.TestCase):
    """Test dell'handler API che ritorna JSON."""

    @patch('countdown.date')
    def test_handle_request_success_future(self, mock_date):
        """Test: handle_request ritorna JSON valido con status success per data futura."""
        mock_date.today.return_value = date(2026, 1, 1)

        # Chiama handle_request con parametri diretti
        response_json = handle_request('2026-12-31', 'Fine Anno')

        # Deve essere una stringa JSON
        self.assertIsInstance(response_json, str)

        # Deve contenere i campi chiave
        self.assertIn('"status"', response_json)
        self.assertIn('"success"', response_json)
        self.assertIn('"data"', response_json)

    @patch('countdown.date')
    def test_handle_request_json_structure(self, mock_date):
        """Test: JSON response ha struttura corretta."""
        import json
        mock_date.today.return_value = date(2026, 1, 1)

        # Chiama handle_request con parametri diretti
        response_json = handle_request('2026-06-15', 'Evento Estate')
        data = json.loads(response_json)

        # Verifica struttura
        self.assertEqual(data["status"], "success")
        self.assertIn("data", data)
        self.assertIn("days_remaining", data["data"])
        self.assertIn("target_date", data["data"])
        self.assertIn("event_name", data["data"])
        self.assertIn("is_past", data["data"])
        self.assertIn("is_today", data["data"])

    @patch('countdown.date')
    def test_handle_request_error_invalid_date(self, mock_date):
        """Test: Data invalida ritorna error response."""
        import json
        mock_date.today.return_value = date(2026, 1, 1)

        # Chiama handle_request con data invalida
        response_json = handle_request('data-invalida', 'Evento')
        data = json.loads(response_json)

        # Verifica errore
        self.assertEqual(data["status"], "error")
        self.assertIn("message", data)


class TestEdgeCases(unittest.TestCase):
    """Test casi limite e boundary conditions."""

    @patch('countdown.date')
    def test_cambio_anno(self, mock_date):
        """Test: Countdown attraverso cambio anno (31 Dec → 1 Gen)."""
        mock_date.today.return_value = date(2025, 12, 31)

        result = get_countdown("2026-01-01", "Capodanno")

        self.assertEqual(result["days_remaining"], 1)
        self.assertFalse(result["is_past"])

    @patch('countdown.date')
    def test_anno_bisestile(self, mock_date):
        """Test: Countdown che attraversa anno bisestile."""
        mock_date.today.return_value = date(2024, 2, 28)

        result = get_countdown("2024-03-01", "Post-Bisestile")

        # 2024 è bisestile, quindi 28 Feb → 1 Mar = 2 giorni
        self.assertEqual(result["days_remaining"], 2)

    @patch('countdown.date')
    def test_data_molto_futura(self, mock_date):
        """Test: Data molto lontana nel futuro."""
        mock_date.today.return_value = date(2026, 1, 1)

        result = get_countdown("2030-01-01", "Futuro Lontano")

        # Calcolo: 4 anni = ~1461 giorni (con bisestile)
        self.assertGreater(result["days_remaining"], 1400)
        self.assertFalse(result["is_past"])

    @patch('countdown.date')
    def test_data_molto_passata(self, mock_date):
        """Test: Data molto lontana nel passato."""
        mock_date.today.return_value = date(2026, 1, 1)

        result = get_countdown("2020-01-01", "Passato Lontano")

        # Calcolo: ~6 anni fa
        self.assertLess(result["days_remaining"], -2000)
        self.assertTrue(result["is_past"])

    @patch('countdown.date')
    def test_date_format_variants(self, mock_date):
        """Test: Diversi formati di data (se supportati)."""
        mock_date.today.return_value = date(2026, 1, 1)

        # Formato standard YYYY-MM-DD
        result = get_countdown("2026-01-15")
        self.assertEqual(result["days_remaining"], 14)

    @patch('countdown.date')
    def test_event_name_empty_string(self, mock_date):
        """Test: Event name stringa vuota → accettato (stringa vuota valida)."""
        mock_date.today.return_value = date(2026, 1, 1)

        result = get_countdown("2026-01-10", "")

        # Stringa vuota è un valore valido
        self.assertEqual(result["event_name"], "")

    @patch('countdown.date')
    def test_event_name_long(self, mock_date):
        """Test: Event name molto lungo."""
        mock_date.today.return_value = date(2026, 1, 1)

        long_name = "Evento con nome estremamente lungo per testare limiti" * 3
        result = get_countdown("2026-01-10", long_name)

        # Dovrebbe accettare il nome (o troncarlo se c'è limite)
        self.assertIsInstance(result["event_name"], str)

    @patch('countdown.date')
    def test_stato_flags_consistency(self, mock_date):
        """Test: is_past e is_today sono mutuamente esclusivi."""
        mock_date.today.return_value = date(2026, 1, 1)

        # Test per ogni scenario
        scenarios = [
            ("2026-01-05", False, False),  # futuro
            ("2026-01-01", False, True),   # oggi
            ("2025-12-20", True, False),   # passato
        ]

        for target_date, expected_past, expected_today in scenarios:
            with self.subTest(target_date=target_date):
                result = get_countdown(target_date)
                self.assertEqual(result["is_past"], expected_past)
                self.assertEqual(result["is_today"], expected_today)

                # is_past e is_today non possono essere entrambi True
                self.assertFalse(result["is_past"] and result["is_today"])


def run_tests():
    """Esegue la suite di test con output dettagliato."""
    print("=" * 70)
    print("TEST SUITE: Countdown Feature")
    print("=" * 70)
    print()

    # Crea test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Aggiungi tutti i test
    suite.addTests(loader.loadTestsFromTestCase(TestCountdownLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestHandleRequest))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))

    # Esegui con verbosity alta
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Riepilogo finale
    print()
    print("=" * 70)
    print("RIEPILOGO TEST")
    print("=" * 70)
    print(f"Test eseguiti: {result.testsRun}")
    print(f"Successi: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallimenti: {len(result.failures)}")
    print(f"Errori: {len(result.errors)}")
    print()

    if result.wasSuccessful():
        print("✅ TUTTI I TEST PASSANO!")
    else:
        print("❌ CI SONO TEST FALLITI!")

    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
