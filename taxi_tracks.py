def show_tracks(taxi_id):

    # Calcular o tamanho da figura
    sql ="""
            select st_astext(st_envelope(st_collect(st_simplify(proj_boundary,100,FALSE))))
            from cont_aad_caop2018
            where concelho='PORTO';
         """

    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()

    row = results[0]
    polygon_string = row[0]
    xs,ys = polygon_to_points(polygon_string)
    width_in_inches = ((max(xs)-min(xs))/0.0254)*1.1
    height_in_inches = ((max(ys)-min(ys))/0.0254)*1.1
    fig = plt.figure(figsize=(width_in_inches*scale,height_in_inches*scale))


    # Desenhar todos os distritos
    sql ="""
            select st_astext(st_simplify(proj_boundary,100,False))
            from cont_aad_caop2018
            where distrito in ( 'PORTO');
        """

    cursor_psql.execute(sql)
    results = cursor_psql.fetchall()
    for row in results:
        polygon_string = row[0]
        xs, ys = polygon_to_points(polygon_string)
        plt.plot(xs,ys,color='black')


    # Plot tracks
    state_list =[ ("state='FREE'", "green"),
                ("state='BUSY'", "red"),
                ("state='PICKUP'", "yellow"),
                ("state='PAUSE'", "grey") ]
    for tupple in state_list:
        state, color = tupple

        sql = """ select st_astext(st_startpoint(proj_track))
                  from tracks
                  where taxi='"""+taxi_id+"' and " + state

        cursor_psql.execute(sql)
        results = cursor_psql.fetchall()

        xs, ys = points_list_to_points(results)
        plt.plot(xs,ys, color=color)

    plt.show();
