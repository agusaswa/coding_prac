import sectdes_creator as sd

def main():
    S355 = sd.Grade(355,470,210000,0.3)

    Sect_1 = sd.SectionFromDatabase.create(
        section_type_enum=sd.SectTypeEnum.UC,
        section_name="UC300",grade=S355
        )
    Sect_2 = sd.SectionFromDatabase.create(
        section_type_enum=sd.SectTypeEnum.CHS,
        section_name="CHS100x8.0",grade=S355
        )
    print(Sect_1.sect_data.__dict__)
    print(Sect_2.sect_data.__dict__)
    print(Sect_2.grade.tensile_str)

if __name__ == "__main__":
    main()
