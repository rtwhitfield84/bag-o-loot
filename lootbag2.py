import sys
import sqlite3

class LootBag():


    def add_toy_for_child(self, child, toy):

        """Adds a toy and child (if child deosnt exist) to lootbag database

        Arguments:
         child -- string
         toy -- string

        CommandLine:
         'python lootbag2.py add child toy'

        """
        with sqlite3.connect('lootbag.db') as conn:
            c = conn.cursor()

            try:
                c.execute("INSERT INTO child VALUES (?, ?, ?, ?)",
                    (None, child, 0, "No"))
            except sqlite3.IntegrityError:
            	pass

            c.execute("SELECT childId FROM child WHERE name='{}'".format(child))
            results = c.fetchall()

            try:
                c.execute("INSERT INTO toy VALUES (?, ?, ?)",
                    (None, toy, results[0][0]))
            except sqlite3.OperationalError:
                pass

    def remove_toy_for_child(self, child, toy):

        """Removes a toy from child in lootbag database

        Arguments:
         child -- string
         toy -- string

        CommandLine:
         'python lootbag2.py remove child toy'

        """
        with sqlite3.connect('lootbag.db') as conn:
            c = conn.cursor()

            c.execute("SELECT childId FROM child WHERE name='{}'".format(child))
            results = c.fetchall()

            try:
                c.execute("DELETE FROM toy WHERE childId={} AND name='{}'"
                    .format(results[0][0], toy))
            except sqlite3.OperationalError:
                pass


    def get_by_child(self, child):

        """Prints a list of childs toys from lootbag database

        Arguments:
         child -- string

        CommandLine:
         'python lootbag2.py ls child'

        """

        with sqlite3.connect('lootbag.db') as conn:
            c = conn.cursor()

            c.execute("""SELECT t.Name
                FROM toy t, child c
                WHERE c.Name='{}'
                AND c.childId = t.childId
            """.format(child))

            toys = c.fetchall()
            print(child + "'s Toys: \n " + "\n ".join(str(toy[0]) for toy in toys))


    def get_list_of_kids(self):

        """Prints list of good children from lootbag database

        Arguments:
            None


        CommandLine:
         'python lootbag2.py ls'

        """

        with sqlite3.connect('lootbag.db') as conn:
            c = conn.cursor()

            c.execute("SELECT name FROM child")
            kids = c.fetchall()
            print("Good kids: \n " + "\n ".join(str(kid[0]) for kid in kids))


    def deliver_toys_to_child(self, child):

        """Sets a childs delivered property to true in lootbag database

        Arguments:
         child -- string

        CommandLine:
         'python lootbag2.py deliver child'

        """
        with sqlite3.connect('lootbag.db') as conn:
            c = conn.cursor()

            c.execute("UPDATE child SET happy = 1, delivered = datetime('now') WHERE name = '{}'".format(child))

    def is_child_happy(self, child):

        """Returns if child is happy or not from lootbag database

        Arguments:
         child -- string

        CommandLine:
         'python lootbag2.py happy child'

        """
        with sqlite3.connect('lootbag.db') as conn:
            c = conn.cursor()

            c.execute("SELECT name FROM child WHERE name='{}' and happy= {}".format(child,1))
            happyKid = c.fetchall()
            if len(happyKid) == 0:
                print('Sorry,{} is not a happy camper'.format(child))
            else:
                print('{},is overjoyed!'.format(child))


    def get_happy_kids(self):

        """Returns a list of happy kids from lootbag database

        Arguments:
            None

        CommandLine:
         'python lootbag2.py happyKids'

        """

        with sqlite3.connect('lootbag.db') as conn:
            c = conn.cursor()

            c.execute("SELECT name FROM child WHERE happy != 0")
            happyKids = c.fetchall()
            print("Happy kids: \n " + "\n ".join(str(kid[0]) for kid in happyKids))



    def remove_naughty_child_toys(self, child):

        """Removes a naughty childs toys from child in lootbag database

        Arguments:
         child -- string

        CommandLine:
         'python lootbag2.py naughty child'

        """

        with sqlite3.connect('lootbag.db') as conn:
            c = conn.cursor()

            c.execute("SELECT childId FROM child WHERE name='{}'".format(child))
            results = c.fetchall()

            try:
                c.execute("UPDATE child SET happy = 0, delivered = 'Naughty' WHERE name = '{}'".format(child))
            except sqlite3.OperationalError:
                pass

            try:
                c.execute("DELETE FROM toy WHERE childId={}"
                    .format(results[0][0]))
            except sqlite3.OperationalError:
                pass



if __name__ == "__main__":
    bag = LootBag()

    if len(sys.argv) == 1:
        print("""no arguments specified!\n 
type 'python lootbag2.py help' to see available methods""")
        sys.exit()

    if sys.argv[1] == "add":
        bag.add_toy_for_child(sys.argv[2], sys.argv[3])

    elif sys.argv[1] == "remove":
        bag.remove_toy_for_child(sys.argv[2], sys.argv[3])

    elif len(sys.argv) == 2 and sys.argv[1] == "ls":
        bag.get_list_of_kids()

    elif sys.argv[1] == "ls" and sys.argv[2] == sys.argv[2]:
        bag.get_by_child(sys.argv[2])

    elif sys.argv[1] == "deliver" and sys.argv[2] == sys.argv[2]:
        bag.deliver_toys_to_child(sys.argv[2])

    elif sys.argv[1] == "happy" and sys.argv[2] == sys.argv[2]:
        bag.is_child_happy(sys.argv[2])

    elif sys.argv[1] == "happyKids":
        bag.get_happy_kids()

    elif sys.argv[1] == "naughty" and sys.argv[2] == sys.argv[2]:
        bag.remove_naughty_child_toys(sys.argv[2])

    elif sys.argv[1] =="help":
        print(help(LootBag))

    else:
        print("incorrect arguments given")


