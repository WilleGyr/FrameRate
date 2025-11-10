from database import (
    init_db, add_movie, add_actor_to_movie,
    search_movies, get_movie_details,
    search_actors, get_actor_details,
    top10_movies, top10_actors
)

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

def show_movie_search():
    q = input("\nSök film (del av titel): ").strip()
    results = search_movies(q)
    if not results:
        print("Inga filmer hittades.")
        return
    print("\nResultat:")
    for mid, title, year, overall, combined in results:
        print(f"[{mid}] {title} ({year})  overall={overall}  combined={combined}")
    try:
        pick = int(input("\nAnge film-ID för detaljer (eller blankt för att avbryta): ") or -1)
    except ValueError:
        return
    if pick == -1:
        return
    movie, cast = get_movie_details(pick)
    if not movie:
        print("Ogiltigt film-ID.")
        return
    (mid, title, year, director, runtime_min,
     r_overall, r_emo, r_story, r_vis, r_sound,
     combined, cast_avg, cast_count) = movie
    print("\n— Filmdetaljer —")
    print(f"ID: {mid}")
    print(f"Titel: {title} ({year})")
    print(f"Regissör: {director}")
    print(f"Längd: {runtime_min} min")
    print(f"Ratings: overall={r_overall}, emotional={r_emo}, story={r_story}, visuals={r_vis}, sound={r_sound}")
    print(f"Kombinerad rating: {combined}  (cast-snitt={cast_avg}, antal skådisar={cast_count})")
    print("\nRollista:")
    if not cast:
        print("  –")
    else:
        for name, role, ar in cast:
            role_txt = f" som {role}" if role else ""
            print(f"  {name}{role_txt} — prestation: {ar}")

def show_actor_search():
    q = input("\nSök skådis (del av namn): ").strip()
    results = search_actors(q)
    if not results:
        print("Inga skådisar hittades.")
        return

    # --- OM BARA EN TRÄFF, visa direkt ---
    if len(results) == 1:
        aid, name, rating, roles = results[0]
        summary, roles = get_actor_details(aid)
        print_actor_details(summary, roles)
        return

    # --- annars lista flera alternativ ---
    print("\nResultat:")
    for aid, name, rating, roles in results:
        print(f"[{aid}] {name}  career={rating}  roller={roles}")

    try:
        pick = int(input("\nAnge skådis-ID för detaljer (eller blankt för att avbryta): ") or -1)
    except ValueError:
        return
    if pick == -1:
        return

    summary, roles = get_actor_details(pick)
    if not summary:
        print("Ogiltigt skådis-ID.")
        return
    print_actor_details(summary, roles)

def print_actor_details(summary, roles):
    aid, name, career_rating, roles_count = summary
    print("\n— Skådis —")
    print(f"Namn: {name}")
    print(f"Kombinerad karriärrating: {career_rating}  (roller: {roles_count})")
    print("\nRoller:")
    if not roles:
        print("  –")
    else:
        for mid, title, year, role, ar in roles:
            role_txt = f" som {role}" if role else ""
            print(f"  {title} ({year}){role_txt} — prestation: {ar} [movie_id={mid}]")


def show_top10_movies():
    rows = top10_movies()
    if not rows:
        print("\nInga filmer med overall rating ännu.")
        return
    print("\n— Top 10 Filmer (combined) —")
    for i, (mid, title, year, combined, overall) in enumerate(rows, start=1):
        print(f"{i:>2}. [{mid}] {title} ({year})  combined={combined}  overall={overall}")

def show_top10_actors():
    rows = top10_actors()
    if not rows:
        print("\nInga skådisar ännu.")
        return
    print("\n— Top 10 Skådisar (karriärrating) —")
    for i, (aid, name, rating, roles) in enumerate(rows, start=1):
        print(f"{i:>2}. [{aid}] {name}  career={rating}  roller={roles}")

def main():
    init_db()
    while True:
        print("\n=== Film Logger ===")
        print("1. Logga ny film")
        print("2. Sök film och visa detaljer")
        print("3. Sök skådis och visa detaljer")
        print("4. Top 10 filmer (overall)")
        print("5. Top 10 skådisar (kombinerad)")
        print("6. Avsluta")
        choice = input("Val: ").strip()

        if choice == "1":
            log_movie()
        elif choice == "2":
            show_movie_search()
        elif choice == "3":
            show_actor_search()
        elif choice == "4":
            show_top10_movies()
        elif choice == "5":
            show_top10_actors()
        elif choice == "6":
            print("Hejdå 👋")
            break
        else:
            print("Ogiltigt val, försök igen.")

if __name__ == "__main__":
    main()
