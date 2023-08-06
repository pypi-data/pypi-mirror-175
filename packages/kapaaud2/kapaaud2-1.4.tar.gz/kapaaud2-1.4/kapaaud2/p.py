IF "shou1".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "aa上位机".r_data[#i] = ',' OR "aa上位机".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "aa上位机".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "aa上位机".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
        END_IF;
    END_FOR;
    
    "aa上位机".r_data := "aa上位机".e_data;
    
    IF "aa上位机".u_data[0] = 'start' THEN
        "aa上位机".ewm := "aa上位机".empty;
        "aa上位机".people := "aa上位机".empty;
        "aa上位机".face := 0;
        "物资发放标志" := 1;
        "系统启停" := 1;
    ELSIF "aa上位机".u_data[0] = 'stop' THEN
        "系统启停" := 0;
        "物资发放标志" := 0;
        "皮带正转" := 0;
        "步骤" := 0;
    ELSIF "aa上位机".u_data[0] = 'A' THEN
        "aa上位机".face := STRING_TO_INT("aa上位机".u_data[1]);
        
    ELSIF "aa上位机".u_data[0] = 'B' THEN
        FOR #i := 0 TO 5 DO
            "aa上位机".ewm[#i] := "aa上位机".u_data[#i + 1];
        END_FOR;
    ELSIF "aa上位机".u_data[0] = 'C' THEN
        FOR #i := 0 TO 5 DO
            "aa上位机".people[#i] := "aa上位机".u_data[#i + 2];
        END_FOR;
        IF "aa上位机".u_data[1] = 'low' THEN
            "e发送"(buf := 'A1',
                  num := 4);
        ELSIF "aa上位机".u_data[1] = 'mid' THEN
            "e发送"(buf := 'B1',
                  num := 4);
        ELSIF "aa上位机".u_data[1] = 'high' THEN
            "e发送"(buf := 'C1',
                  num := 4);
        ELSIF "aa上位机".u_data[1] = 'geli' THEN
            "e发送"(buf := 'D1',
                  num := 4);
        END_IF;
    END_IF;
END_IF;

IF "物资发放标志" AND "物料检测" AND "物料到位" = 0 THEN
    "物资发放标志" := 0;
    "步骤" := 4;
END_IF;

/////////////////////
IF "shou3".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "cc视觉".r_data[#i] = ',' OR "cc视觉".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "cc视觉".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "cc视觉".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
        END_IF;
    END_FOR;
    
    "cc视觉".r_data := "cc视觉".e_data;
    
    IF "cc视觉".u_data[0] = 'wz' THEN
        "e发送"(buf := 'ok',
              num := 1);
    END_IF;
END_IF;
///////////////////
IF "shou4".DONE THEN
    FOR #i := 0 TO 61 DO
        IF "dd机器人".r_data[#i] = ',' OR "dd机器人".r_data[#i] = 0 THEN
            Chars_TO_Strg(Chars := "dd机器人".r_data,
                          pChars := #i_1,
                          Cnt := #i - #i_1,
                          Strg => "dd机器人".u_data[#i_2]);
            #i_1 := #i + 1;
            #i_2 += 1;
        END_IF;
    END_FOR;
    
    "dd机器人".r_data := "dd机器人".e_data;
    
    IF "dd机器人".u_data[0] = 'fw' AND "系统启停" THEN
        "物资发放标志" := 1;
    END_IF;
END_IF;
//////////////////////
"发送长度" := LEN(#buf);
IF #num = 1 THEN
    Strg_TO_Chars(Strg := #buf,
                  pChars := 0,
                  Cnt => #len,
                  Chars := "aa上位机".t_data);
    "发送标志" := 1;
ELSIF #num = 3 THEN
    Strg_TO_Chars(Strg := #buf,
                  pChars := 0,
                  Cnt => #len,
                  Chars := "cc视觉".t_data);
    "发送标志" := 1;
ELSIF #num = 4 THEN
    Strg_TO_Chars(Strg := #buf,
                  pChars := 0,
                  Cnt => #len,
                  Chars := "dd机器人".t_data);
    "发送标志" := 1;
END_IF;
            
        