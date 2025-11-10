from database import init_db, add_movie, add_actor_to_movie

def log_movie():
    print("\n🎥 Lägg till en ny film")
    title = input("Titel: ")
    year = int(input("År: "))
    director = input("Regissör: ")
    runtime_min = int(input("Längd (minuter): "))

    print("\n--- Betyg (1–5) ---")
    rating_overall = float(input("Helhetsbetyg: "))
    rating_emotional = float(input("Känslomässigt betyg: "))
    rating_story = float(input("Story-betyg: "))
    rating_visuals = float(input("Visuellt betyg: "))
    rating_sound = float(input("Ljud-betyg: "))

    movie_id = add_movie(title, year, director, runtime_min,
                         rating_overall, rating_emotional,
                         rating_story, rating_visuals, rating_sound)

    print(f"\n✅ Filmen '{title}' har lagts till med ID {movie_id}.")

    # Lägg till skådespelare
    while True:
        add_actor = input("\nVill du lägga till en skådespelare? (j/n): ").lower()
        if add_actor != "j":
            break
        actor_name = input("Namn: ")
        character_name = input("Rollnamn (valfritt): ") or None
        actor_rating = float(input("Betyg för denna prestation (1–5): "))

        add_actor_to_movie(movie_id, actor_name, character_name, actor_rating)
        print(f"⭐ Lagt till {actor_name} i '{title}'")

    print("\n🎬 Film loggad!")

def main():
    init_db()
    while True:
        print("\n=== Film Logger ===")
        print("1. Logga ny film")
        print("2. Avsluta")
        choice = input("Val: ")

        if choice == "1":
            log_movie()
        elif choice == "2":
            print("Hejdå 👋")
            break
        else:
            print("Ogiltigt val, försök igen.")

if __name__ == "__main__":
    main()
