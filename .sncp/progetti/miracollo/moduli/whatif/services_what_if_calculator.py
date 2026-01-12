"""
What-If Pricing Simulator - Calculator Service
Modulo: What-If Simulator
Versione: 1.0.0
Data: 12 Gennaio 2026

DESTINAZIONE: backend/services/what_if_calculator.py

Formula Elasticity:
- elasticity = -0.5 (standard hotel)
- Se prezzo +10% -> occupancy -5%
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-12"

from datetime import date, datetime
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class WhatIfCalculator:
    """
    Calcola l'impatto di variazioni prezzo su occupancy e revenue.

    Usa formula elasticity-based per MVP.
    Futuro: sostituire con modello ML.
    """

    # Elasticity standard per hotel (-0.5 = se prezzo +10%, domanda -5%)
    DEFAULT_ELASTICITY = -0.5

    def __init__(self, db):
        """
        Inizializza calculator con connessione database.

        Args:
            db: Database session (SQLAlchemy)
        """
        self.db = db
        self.elasticity = self.DEFAULT_ELASTICITY

    def calculate_impact(
        self,
        property_id: int,
        date_target: date,
        room_type_id: int,
        price_adjustment: float
    ) -> Dict[str, Any]:
        """
        Calcola impatto di un cambio prezzo.

        Args:
            property_id: ID della property
            date_target: Data target
            room_type_id: ID tipo camera
            price_adjustment: Variazione prezzo (-1.0 a 1.0)

        Returns:
            Dict con tutti i dati dell'impatto
        """
        try:
            # 1. Ottieni dati attuali
            current_price = self._get_current_price(property_id, date_target, room_type_id)
            current_occupancy = self._get_current_occupancy(property_id, date_target)
            total_rooms = self._get_total_rooms(property_id, room_type_id)

            # 2. Calcola nuovo prezzo
            new_price = current_price * (1 + price_adjustment)

            # 3. Calcola impatto occupancy (elasticity-based)
            occupancy_change = self.elasticity * price_adjustment
            new_occupancy = current_occupancy * (1 + occupancy_change)

            # Clamp occupancy tra 0 e 1
            new_occupancy = max(0.0, min(1.0, new_occupancy))

            # 4. Calcola revenue
            current_revenue = current_price * current_occupancy * total_rooms
            new_revenue = new_price * new_occupancy * total_rooms

            # 5. Competitor position
            competitor_avg = self._get_competitor_avg_price(property_id, date_target)
            position = self._determine_position(new_price, competitor_avg)

            # 6. Confidence score
            confidence = self._calculate_confidence(property_id, date_target, current_occupancy)

            # 7. Generate explanation
            explanation = self._generate_explanation(
                current_price=current_price,
                new_price=new_price,
                current_occupancy=current_occupancy,
                new_occupancy=new_occupancy,
                current_revenue=current_revenue,
                new_revenue=new_revenue,
                position=position,
                competitor_avg=competitor_avg
            )

            return {
                "current_price": round(current_price, 2),
                "new_price": round(new_price, 2),
                "current_occupancy": round(current_occupancy, 4),
                "predicted_occupancy": round(new_occupancy, 4),
                "occupancy_delta": round(new_occupancy - current_occupancy, 4),
                "current_revenue": round(current_revenue, 2),
                "predicted_revenue": round(new_revenue, 2),
                "revenue_delta": round(new_revenue - current_revenue, 2),
                "competitor_position": position,
                "competitor_avg": round(competitor_avg, 2) if competitor_avg else 0,
                "confidence": confidence,
                "explanation": explanation
            }

        except Exception as e:
            logger.error(f"Errore calcolo What-If: {e}")
            raise ValueError(f"Errore nel calcolo: {str(e)}")

    def generate_price_curve(
        self,
        property_id: int,
        date_target: date,
        room_type_id: int,
        min_adjustment: float = -0.30,
        max_adjustment: float = 0.50,
        step: float = 0.05
    ) -> Dict[str, Any]:
        """
        Genera curva price vs occupancy per grafico.

        Args:
            property_id: ID property
            date_target: Data target
            room_type_id: ID tipo camera
            min_adjustment: Variazione minima (default -30%)
            max_adjustment: Variazione massima (default +50%)
            step: Step tra punti (default 5%)

        Returns:
            Dict con current_price e lista punti curva
        """
        current_price = self._get_current_price(property_id, date_target, room_type_id)
        competitor_avg = self._get_competitor_avg_price(property_id, date_target)

        points = []
        adjustment = min_adjustment

        while adjustment <= max_adjustment:
            result = self.calculate_impact(
                property_id=property_id,
                date_target=date_target,
                room_type_id=room_type_id,
                price_adjustment=adjustment
            )

            points.append({
                "price": result["new_price"],
                "occupancy": result["predicted_occupancy"],
                "revenue": result["predicted_revenue"],
                "adjustment_percent": round(adjustment * 100, 1)
            })

            adjustment += step

        return {
            "current_price": current_price,
            "points": points,
            "competitor_avg": competitor_avg
        }

    # ==================== HELPER METHODS ====================

    def _get_current_price(
        self,
        property_id: int,
        date_target: date,
        room_type_id: int
    ) -> float:
        """
        Ottiene prezzo corrente dal database.

        Query: daily_rates o pricing_history
        """
        try:
            # Query per prezzo corrente
            # TODO: Adattare alla struttura DB reale
            query = """
                SELECT rate
                FROM daily_rates
                WHERE property_id = :property_id
                AND date = :date_target
                AND room_type_id = :room_type_id
                ORDER BY created_at DESC
                LIMIT 1
            """
            result = self.db.execute(
                query,
                {
                    "property_id": property_id,
                    "date_target": date_target,
                    "room_type_id": room_type_id
                }
            ).fetchone()

            if result:
                return float(result[0])

            # Fallback: prezzo base dalla room_type
            fallback_query = """
                SELECT base_rate
                FROM room_types
                WHERE id = :room_type_id
            """
            fallback = self.db.execute(
                fallback_query,
                {"room_type_id": room_type_id}
            ).fetchone()

            if fallback:
                return float(fallback[0])

            # Default se non trovato
            logger.warning(f"Prezzo non trovato per property={property_id}, usando default 100")
            return 100.0

        except Exception as e:
            logger.error(f"Errore get_current_price: {e}")
            return 100.0  # Fallback sicuro

    def _get_current_occupancy(
        self,
        property_id: int,
        date_target: date
    ) -> float:
        """
        Ottiene occupancy corrente/prevista.

        Usa booking pace o forecast se disponibile.
        """
        try:
            # Query per occupancy prevista
            query = """
                SELECT occupancy_rate
                FROM occupancy_forecast
                WHERE property_id = :property_id
                AND date = :date_target
                ORDER BY created_at DESC
                LIMIT 1
            """
            result = self.db.execute(
                query,
                {
                    "property_id": property_id,
                    "date_target": date_target
                }
            ).fetchone()

            if result:
                return float(result[0])

            # Fallback: calcola da prenotazioni esistenti
            booking_query = """
                SELECT
                    CAST(COUNT(*) AS FLOAT) /
                    (SELECT total_rooms FROM properties WHERE id = :property_id)
                FROM bookings
                WHERE property_id = :property_id
                AND check_in <= :date_target
                AND check_out > :date_target
                AND status = 'confirmed'
            """
            booking_result = self.db.execute(
                booking_query,
                {
                    "property_id": property_id,
                    "date_target": date_target
                }
            ).fetchone()

            if booking_result and booking_result[0]:
                return min(1.0, float(booking_result[0]))

            # Default se non trovato
            logger.warning(f"Occupancy non trovata per property={property_id}, usando default 0.7")
            return 0.70  # 70% default

        except Exception as e:
            logger.error(f"Errore get_current_occupancy: {e}")
            return 0.70

    def _get_total_rooms(
        self,
        property_id: int,
        room_type_id: int
    ) -> int:
        """Ottiene numero totale camere per tipo."""
        try:
            query = """
                SELECT room_count
                FROM room_types
                WHERE id = :room_type_id
                AND property_id = :property_id
            """
            result = self.db.execute(
                query,
                {
                    "room_type_id": room_type_id,
                    "property_id": property_id
                }
            ).fetchone()

            if result:
                return int(result[0])

            # Fallback: tutte le camere della property
            fallback_query = """
                SELECT total_rooms
                FROM properties
                WHERE id = :property_id
            """
            fallback = self.db.execute(
                fallback_query,
                {"property_id": property_id}
            ).fetchone()

            if fallback:
                return int(fallback[0])

            logger.warning(f"Rooms non trovate per property={property_id}, usando default 50")
            return 50  # Default

        except Exception as e:
            logger.error(f"Errore get_total_rooms: {e}")
            return 50

    def _get_competitor_avg_price(
        self,
        property_id: int,
        date_target: date
    ) -> Optional[float]:
        """Ottiene prezzo medio competitor."""
        try:
            query = """
                SELECT AVG(price)
                FROM competitor_prices
                WHERE property_id = :property_id
                AND date = :date_target
            """
            result = self.db.execute(
                query,
                {
                    "property_id": property_id,
                    "date_target": date_target
                }
            ).fetchone()

            if result and result[0]:
                return float(result[0])

            # Nessun dato competitor
            return None

        except Exception as e:
            logger.error(f"Errore get_competitor_avg_price: {e}")
            return None

    def _determine_position(
        self,
        our_price: float,
        competitor_avg: Optional[float]
    ) -> str:
        """
        Determina posizione rispetto a competitor.

        Returns: "above", "match", "below"
        """
        if competitor_avg is None:
            return "unknown"

        ratio = our_price / competitor_avg

        if ratio > 1.05:  # Più di 5% sopra
            return "above"
        elif ratio < 0.95:  # Più di 5% sotto
            return "below"
        else:
            return "match"

    def _calculate_confidence(
        self,
        property_id: int,
        date_target: date,
        current_occupancy: float
    ) -> str:
        """
        Calcola livello di confidence della previsione.

        Fattori:
        - Lead time (giorni da oggi)
        - Booking pace (quanto siamo vicini alla data)
        - Dati storici disponibili

        Returns: "low", "medium", "high"
        """
        try:
            today = datetime.now().date()
            lead_time = (date_target - today).days

            # Lead time score
            if lead_time < 0:
                return "low"  # Data passata
            elif lead_time <= 7:
                lead_score = 3  # Alta confidenza, pochi giorni
            elif lead_time <= 30:
                lead_score = 2  # Media
            else:
                lead_score = 1  # Bassa, troppo lontano

            # Occupancy score (se alta, più prevedibile)
            if current_occupancy >= 0.7:
                occ_score = 3
            elif current_occupancy >= 0.4:
                occ_score = 2
            else:
                occ_score = 1

            # Score totale
            total_score = lead_score + occ_score

            if total_score >= 5:
                return "high"
            elif total_score >= 3:
                return "medium"
            else:
                return "low"

        except Exception as e:
            logger.error(f"Errore calculate_confidence: {e}")
            return "medium"

    def _generate_explanation(
        self,
        current_price: float,
        new_price: float,
        current_occupancy: float,
        new_occupancy: float,
        current_revenue: float,
        new_revenue: float,
        position: str,
        competitor_avg: Optional[float]
    ) -> str:
        """
        Genera spiegazione testuale per l'utente.

        Template-based, chiaro e conciso.
        """
        # Calcola percentuali
        price_change_pct = ((new_price - current_price) / current_price) * 100
        occ_change_pct = ((new_occupancy - current_occupancy) / current_occupancy) * 100 if current_occupancy > 0 else 0
        rev_change_pct = ((new_revenue - current_revenue) / current_revenue) * 100 if current_revenue > 0 else 0

        # Costruisci spiegazione
        parts = []

        # Parte prezzo
        if price_change_pct > 0:
            parts.append(f"Con prezzo EUR {new_price:.0f} (+{price_change_pct:.0f}%)")
        else:
            parts.append(f"Con prezzo EUR {new_price:.0f} ({price_change_pct:.0f}%)")

        # Parte occupancy
        if occ_change_pct > 0:
            parts.append(f"prevedo occupancy {new_occupancy*100:.0f}% (+{occ_change_pct:.0f}%)")
        else:
            parts.append(f"prevedo occupancy {new_occupancy*100:.0f}% ({occ_change_pct:.0f}%)")

        # Parte revenue
        if rev_change_pct > 0:
            parts.append(f"e revenue EUR {new_revenue:.0f} (+{rev_change_pct:.0f}%)")
        else:
            parts.append(f"e revenue EUR {new_revenue:.0f} ({rev_change_pct:.0f}%)")

        # Parte competitor
        if competitor_avg and position != "unknown":
            position_text = {
                "above": "sopra media competitor",
                "match": "in linea con competitor",
                "below": "sotto media competitor"
            }
            parts.append(f"Posizione: {position_text.get(position, position)} (EUR {competitor_avg:.0f})")

        return ". ".join(parts) + "."
