import streamlit as st
import pandas as pd
import numpy as np
import random
from collections import defaultdict, Counter
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder


col1, col_spacer, col3 = st.columns([2, 7, 1], gap="small")

with col1:
    generate_clicked = st.button("Buat Jadwal Genap Otomatis")

with col3:
    export_clicked = st.button("Export")


# Container untuk hasil tabel agar tampil di bawah tombol-tombol
table_container = st.container()

# Jika tombol "Buat Jadwal" diklik
if generate_clicked:
    with st.spinner("Wait for it..."):
        progress_bar = st.progress(0)
        # Load data CSV dari folder lokal
        courses_df = pd.read_csv('dataset/courses.csv')
        lecturers_df = pd.read_csv('dataset/lecturers.csv')
        rooms_df = pd.read_csv('dataset/rooms.csv')
        timeslots_df = pd.read_csv('dataset/timeslots.csv')

        # Filter periode ganjil
        courses = courses_df[courses_df["periode"] == "Genap"].to_dict(orient="records")
        rooms = rooms_df["id_ruang"].tolist()
        timeslots = timeslots_df.to_dict(orient="records")

        # Global Variabel Slot
        slot_time_map, slot_to_day, timeslots_by_day = {}, {}, defaultdict(list)
        lecturer_sks_limit = dict(zip(lecturers_df["id_dosen"], lecturers_df["max_sks_per_day"]))
        for slot in timeslots:
            start = datetime.strptime(slot["mulai"], "%H:%M").time()
            end = datetime.strptime(slot["selesai"], "%H:%M").time()
            slot_tuple = (slot["id_slot"], start, end)
            timeslots_by_day[slot["hari"]].append(slot_tuple)
            slot_time_map[slot["id_slot"]] = slot_tuple
            slot_to_day[slot["id_slot"]] = slot["hari"]
        for hari in timeslots_by_day:
            timeslots_by_day[hari].sort(key=lambda x: x[1])

        POP_SIZE, GENERATIONS, MUTATION_RATE, TOURNAMENT_SIZE = 200, 300, 0.1, 5

        def get_consecutive_slots(hari, count, usage_counter):
            slots = sorted(timeslots_by_day[hari], key=lambda x: usage_counter[x[0]])
            for i in range(len(slots) - count + 1):
                group = slots[i:i+count]
                if all(group[j][2] <= group[j+1][1] for j in range(count - 1)):
                    return [slot[0] for slot in group]
            return None

        def weighted_choice(items, counter):
            weights = [1 / (1 + counter[item]) for item in items]
            return random.choices(items, weights=weights, k=1)[0]

        def generate_individual():
            individual, unplaced_log = [], []
            room_slot_usage = set()
            dosen_slot_usage = set()
            dosen_sks_per_day = defaultdict(lambda: defaultdict(int))
            student_slot_usage = defaultdict(set)
            global_slot_usage = Counter()

            for course in courses:
                id_mk = course["id_mk"]
                id_dosen = course["id_dosen"]
                sks = course["sks"]
                kelas = course["kelas"]
                semester = course["semester"]
                assigned = False

                for _ in range(30):
                    hari = weighted_choice(list(timeslots_by_day.keys()), global_slot_usage)
                    slots = get_consecutive_slots(hari, sks, global_slot_usage)
                    if not slots: continue
                    room = weighted_choice(rooms, global_slot_usage)

                    if any((room, slot) in room_slot_usage for slot in slots): continue
                    if any((id_dosen, slot) in dosen_slot_usage for slot in slots): continue
                    if dosen_sks_per_day[id_dosen][hari] + sks > lecturer_sks_limit.get(id_dosen, 6): continue
                    if any((kelas, semester, slot) in student_slot_usage for slot in slots): continue

                    for slot in slots:
                        room_slot_usage.add((room, slot))
                        dosen_slot_usage.add((id_dosen, slot))
                        student_slot_usage[(kelas, semester, slot)].add(id_mk)
                        global_slot_usage[slot] += 1

                    dosen_sks_per_day[id_dosen][hari] += sks
                    individual.append({"id_mk": id_mk, "id_dosen": id_dosen, "sks": sks, "room": room, "timeslots": slots})
                    assigned = True
                    break

                if not assigned:
                    unplaced_log.append(f"Gagal menjadwalkan {id_mk} (Dosen: {id_dosen}, SKS: {sks})")

            return individual, unplaced_log

        def calculate_fitness(individual):
            conflicts = 0
            room_time, dosen_time, student_time = defaultdict(list), defaultdict(list), defaultdict(list)
            dosen_sks_per_day = defaultdict(lambda: defaultdict(int))

            for gene in individual:
                id_mk = gene["id_mk"]
                id_dosen = gene["id_dosen"]
                room = gene["room"]
                sks = gene["sks"]
                timeslots = gene["timeslots"]
                hari = slot_to_day[timeslots[0]]
                course_info = next(c for c in courses if c["id_mk"] == id_mk)
                kelas, semester = course_info["kelas"], course_info["semester"]

                for slot in timeslots:
                    room_time[(room, slot)].append(id_mk)
                    dosen_time[(id_dosen, slot)].append(id_mk)
                    student_time[(kelas, semester, slot)].append(id_mk)
                dosen_sks_per_day[id_dosen][hari] += sks

            for v in room_time.values(): conflicts += len(v) - 1 if len(v) > 1 else 0
            for v in dosen_time.values(): conflicts += len(v) - 1 if len(v) > 1 else 0
            for v in student_time.values(): conflicts += len(v) - 1 if len(v) > 1 else 0
            for dosen, perhari in dosen_sks_per_day.items():
                for hari, total in perhari.items():
                    if total > lecturer_sks_limit.get(dosen, 6): conflicts += total - lecturer_sks_limit[dosen]

            return 1 / (1 + conflicts)

        def tournament_selection(pop, fits):
            selected = random.sample(list(zip(pop, fits)), TOURNAMENT_SIZE)
            return max(selected, key=lambda x: x[1])[0]

        def crossover(p1, p2):
            pt = random.randint(1, min(len(p1), len(p2)) - 1)
            return p1[:pt] + p2[pt:], p2[:pt] + p1[pt:]

        def mutate(ind):
            for gene in ind:
                if random.random() < MUTATION_RATE:
                    hari = random.choice(list(timeslots_by_day.keys()))
                    new_slots = get_consecutive_slots(hari, gene["sks"], Counter())
                    if new_slots:
                        gene["timeslots"] = new_slots
                if random.random() < MUTATION_RATE:
                    gene["room"] = random.choice(rooms)
            return ind

        def run_genetic_algorithm():
            population, logs_all = [], []
            for _ in range(POP_SIZE):
                ind, logs = generate_individual()
                population.append(ind)
                logs_all.append(logs)

            best_sol, best_fit, best_log = None, 0, []
            for _ in range(GENERATIONS):
                fitnesses = [calculate_fitness(ind) for ind in population]
                max_fit = max(fitnesses)
                if max_fit > best_fit:
                    best_fit = max_fit
                    best_sol = population[fitnesses.index(max_fit)]
                    best_log = logs_all[fitnesses.index(max_fit)]

                new_pop = [best_sol]
                while len(new_pop) < POP_SIZE:
                    p1, p2 = tournament_selection(population, fitnesses), tournament_selection(population, fitnesses)
                    c1, c2 = crossover(p1, p2)
                    new_pop.append(mutate(c1))
                    if len(new_pop) < POP_SIZE:
                        new_pop.append(mutate(c2))
                population = new_pop
                progress_bar.progress((_ + 1) / GENERATIONS)

            return best_sol, best_fit, best_log

    # Setelah semua fungsi ditulis ulang: jalankan
    best_schedule, best_score, unplaced_logs = run_genetic_algorithm()

    st.success(f"Fitness terbaik: {best_score}")
    st.write(f"Jumlah matkul terjadwal: {len(best_schedule)} / {len(courses)}")

    # if unplaced_logs:
    #     st.warning("Beberapa matkul gagal dijadwalkan:")
    #     for log in unplaced_logs:
    #         st.text("- " + log)
    # else:
    #     st.success("Semua matkul berhasil dijadwalkan!")

    # Tampilkan jadwal yang berhasil
    # st.subheader("📋 Jadwal Otomatis:")
    # schedule_df = pd.DataFrame(best_schedule)
    # st.dataframe(schedule_df, use_container_width=True)

    # Tampilkan di container
    with table_container:
        # Mapping ID ke nama
        id_mk_to_name = dict(zip(courses_df["id_mk"], courses_df["nama_mk"]))
        id_dosen_to_name = dict(zip(lecturers_df["id_dosen"], lecturers_df["nama_dosen"]))
        id_mk_to_kelas = dict(zip(courses_df["id_mk"], courses_df["kelas"]))
        id_mk_to_sks = dict(zip(courses_df["id_mk"], courses_df["sks"]))
        id_mk_to_semester = dict(zip(courses_df["id_mk"], courses_df["semester"]))

        # Struktur hari -> slot -> room
        jadwal_hari = defaultdict(lambda: defaultdict(dict))
        for entry in best_schedule:
            id_mk = entry["id_mk"]
            id_dosen = entry["id_dosen"]
            room = entry["room"]
            slots = entry["timeslots"]
            hari = slot_to_day[slots[0]]
            matkul = id_mk_to_name.get(id_mk, id_mk)
            dosen = id_dosen_to_name.get(id_dosen, id_dosen)
            kelas = id_mk_to_kelas.get(id_mk, "-")
            sks = id_mk_to_sks.get(id_mk, "-")
            semester = id_mk_to_semester.get(id_mk, "-")

            for slot in slots:
                slot_index = int(slot[1:])  # contoh 'T10' → 10
                isi = f"{matkul}\n{dosen}\n{kelas} - {sks} SKS - Smt {semester}"
                jadwal_hari[hari][slot_index][room] = isi

        # Konversi jadwal_hari ke tabel DataFrame
        tabel_jadwal = []
        ordered_days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]

        for hari in ordered_days:
            if hari not in timeslots_by_day:
                continue

            slot_list = sorted(timeslots_by_day[hari], key=lambda x: int(x[0][1:]))
            for sid, mulai, selesai in slot_list:
                slot_index = int(sid[1:])
                waktu_str = f"{mulai.strftime('%H:%M')} - {selesai.strftime('%H:%M')}"
                row = {
                    "Hari": hari,
                    "Slot": f"Slot {slot_index}",
                    "Waktu": waktu_str
                }

                for room in rooms:
                    row[room] = jadwal_hari[hari].get(slot_index, {}).get(room, "")

                tabel_jadwal.append(row)

        df_jadwal = pd.DataFrame(tabel_jadwal)
        # Konfigurasi AgGrid agar text wrap dan kolom otomatis menyesuaikan tinggi
        gb = GridOptionsBuilder.from_dataframe(df_jadwal)
        gb.configure_default_column(wrapText=True, autoHeight=True)
        gb.configure_grid_options(domLayout='normal')  # penting agar tinggi sel bisa mengikuti konten

        # Tampilkan jadwal dengan AgGrid
        # st.subheader("📅 Jadwal Ganjil Otomatis (Wrap Text + Scroll)")
        AgGrid(
            df_jadwal,
            gridOptions=gb.build(),
            fit_columns_on_grid_load=True,
            height=500,
            enable_enterprise_modules=False
        )

