import random
from algorithms.Algorithm import Algorithm

class WSAT(Algorithm):
    def __init__(self, max_tries=400, max_flips=100, p=0.5):
        super().__init__()
        self.max_tries = max_tries
        self.max_flips = max_flips
        self.p = p
        self.kb = None
        self.query = None

    def infer(self, kb, query):
        self.kb = kb
        self.query = query
        found_satisfying_model = False

        for try_num in range(self.max_tries):
            temp_sol = self.random_assignment()
            best_sol = temp_sol.copy()
            for flip_num in range(self.max_flips):
                unsatisfied_clause = self.choose_unsatisfied_clause(temp_sol)
                if unsatisfied_clause is None:  # All clauses satisfied
                    found_satisfying_model = True  # Mark that we found a model
                    if not self.check_query(best_sol):
                        return  # If this model doesn't entail the query, we are done
                    break  # Move to the next random assignment
                if random.uniform(0, 1) < self.p:
                    self.flip_random_atom(temp_sol, unsatisfied_clause)
                else:
                    self.flip_best_atom(temp_sol, unsatisfied_clause)
                if self.is_better(temp_sol, best_sol):
                    best_sol = temp_sol.copy()

        if found_satisfying_model:
            self.output = "YES"  # If we found at least one model and it entailed the query
        return

    def random_assignment(self):
        """Generates a random truth assignment for the symbols in the KB."""
        model = {}
        for symbol in self.kb.symbols:
            model[symbol] = random.choice([True, False])
        return model

    def choose_unsatisfied_clause(self, model):
        """Chooses a random unsatisfied clause from the KB."""
        unsatisfied_clauses = []
        for sentence in self.kb.sentences:
            sentence.setValue(model)
            if not sentence.result():
                unsatisfied_clauses.append(sentence)
        if unsatisfied_clauses:
            return random.choice(unsatisfied_clauses)
        else:
            return None

    def flip_random_atom(self, model, clause):
        """Flips the truth value of a random atom in the clause."""
        symbol = random.choice(list(clause.symbols))
        model[symbol.getCharacter()] = not model[symbol.getCharacter()]

    def flip_best_atom(self, model, clause):
        """Flips the atom in the clause that leads to the best improvement."""
        best_symbol = None
        best_satisfied_count = -1

        for symbol in clause.symbols:
            temp_model = model.copy()
            temp_model[symbol.getCharacter()] = not temp_model[symbol.getCharacter()]
            satisfied_count = self.count_satisfied_clauses(temp_model)

            if satisfied_count > best_satisfied_count:
                best_satisfied_count = satisfied_count
                best_symbol = symbol

        if best_symbol is not None:
            model[best_symbol.getCharacter()] = not model[best_symbol.getCharacter()]

    def is_better(self, model1, model2):
        """Determines if model1 is better than model2 (satisfies more clauses)."""
        return self.count_satisfied_clauses(model1) > self.count_satisfied_clauses(model2)

    def count_satisfied_clauses(self, model):
        """Counts the number of satisfied clauses under a given model."""
        satisfied_count = 0
        for sentence in self.kb.sentences:
            sentence.setValue(model)
            if sentence.result():
                satisfied_count += 1
        return satisfied_count

    def check_query(self, model):
        """Checks if the query is True under the given model."""
        self.query.setValue(model)
        return self.query.result()