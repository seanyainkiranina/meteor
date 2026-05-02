""" Handle saving scores """
import sqlite3


class Score:
    """score handler"""
    def __init__(self, value=0):
        """assign score to save"""
        self.value = value



    def reset(self):
        """reset score to zero"""
        self.value = 0

    def get(self):
        """get score"""
        return self.value

    def get_scores(self):
        """get scores"""
        score_board = []
        score_counter = 0
        last_value =0
        db_path = "lib/scores.db"
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT value FROM scores order by value desc")

        # Loop through the rows
        for row in cursor.fetchall():
            score_counter += 1
            if score_counter<11:
                last_value = row[0]
                score_board.append(str(score_counter) + " "  + str(int(round(row[0],0))))

        cursor.execute("delete from scores where value <" + str(last_value) )
        connection.commit()


        connection.close()
        return score_board

    def save(self):
        """save data to table"""
        db_path = "lib/scores.db"
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(
            """
                INSERT INTO scores (value) VALUES (?)
        """,
            (float(self.value),)
        )
        connection.commit()
        connection.close()
