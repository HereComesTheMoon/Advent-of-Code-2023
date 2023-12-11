fn main() {
    println!("Hello, world!");
    println!("SILVER: The example result is : {}", silver("test1.txt"));
    println!("SILVER: The example result is : {}", silver("test2.txt"));
    println!("SILVER: The result is : {}", silver("input.txt"));
    println!("GOLD: The example result is : {}", gold("test1.txt"));
    println!("GOLD: The example result is : {}", gold("test2.txt"));
    println!("GOLD: The example result is : {}", gold("test3.txt"));
    println!("GOLD: The example result is : {}", gold("test4.txt"));
    println!("GOLD: The result is : {}", gold("input.txt"));
    // not 524, nor 13904
}

fn read(loc: &str) -> Vec<Vec<u8>> {
    std::fs::read_to_string(loc)
        .unwrap()
        .lines()
        .map(|line| line.as_bytes().to_vec())
        .collect()
}

#[derive(Debug, Clone, Copy, Eq, PartialEq)]
struct Pt {
    x: usize,
    y: usize,
}

// fn get_neighbors(grid: Vec<Vec<u8>>, x: usize, y: usize) -> Vec<(usize, usize)> {
//     let val = grid[y][x];
//     let x = x as isize;
//     let y = y as isize;
//     let close = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)];
//     close
//         .iter()
//         .filter(|(x, y)| {
//             0 <= *y && *y < grid.len() as isize && 0 <= *x && *x < grid[0].len() as isize
//         })
//         .map(|&(x, y)| (x as usize, y as usize))
//         .collect()
// }

fn find_starting_tiles(grid: &Vec<Vec<u8>>) -> ((usize, usize), Vec<(usize, usize)>) {
    let mut y = 0;
    let mut x = 0;
    for (yy, row) in grid.iter().enumerate() {
        if let Some((xx, _)) = row
            .iter()
            .enumerate()
            .filter(|(_, &val)| val == b'S')
            .next()
        {
            y = yy;
            x = xx;
            break;
        }
    }

    let mut res = vec![];

    if y.checked_add(1).is_some() && [b'|', b'L', b'J'].contains(&grid[y + 1][x]) {
        res.push((y + 1, x))
    }
    if y.checked_sub(1).is_some() && [b'|', b'F', b'7'].contains(&grid[y - 1][x]) {
        res.push((y - 1, x))
    }
    if x.checked_add(1).is_some() && [b'-', b'7', b'J'].contains(&grid[y][x + 1]) {
        res.push((y, x + 1))
    }
    if x.checked_sub(1).is_some() && [b'-', b'F', b'L'].contains(&grid[y][x - 1]) {
        res.push((y, x - 1))
    }

    ((y, x), res)
}

fn walk(grid: &Vec<Vec<u8>>, dist: &mut Vec<Vec<u64>>, steps: u64, x: usize, y: usize) {
    if dist[y][x] <= steps {
        return;
    }
    let next = match grid[y][x] {
        b'-' => [(y, x + 1), (y, x - 1)],
        b'|' => [(y + 1, x), (y - 1, x)],
        b'L' => [(y, x + 1), (y - 1, x)],
        b'J' => [(y - 1, x), (y, x - 1)],
        b'7' => [(y + 1, x), (y, x - 1)],
        b'F' => [(y, x + 1), (y + 1, x)],
        b'S' => return,
        _ => panic!("Should not happen"),
    };
    // println!("At pos: ({x}, {y}). Val: {}. Steps: {steps}", grid[y][x] as char);
    dist[y][x] = steps;

    for &(y, x) in next.iter() {
        walk(grid, dist, steps + 1, x, y)
    }
}

fn silver(loc: &str) -> u64 {
    let grid = read(loc);

    let start = find_start(&grid);
    let mut prev = start;
    let mut now = get_next(&grid, prev, prev);
    let mut steps = 1;
    while now != start {
        let next = get_next(&grid, prev, now);
        prev = now;
        now = next;
        steps += 1;
    }

    steps / 2
}

fn find_start(grid: &Vec<Vec<u8>>) -> Pt {
    for (y, row) in grid.iter().enumerate() {
        if let Some((x, _)) = row
            .iter()
            .enumerate()
            .filter(|(_, &val)| val == b'S')
            .next()
        {
            return Pt { x, y };
        }
    }

    unreachable!("Oh no!")
}

fn get_next(grid: &Vec<Vec<u8>>, prev: Pt, now: Pt) -> Pt {
    let Pt { x, y } = now;
    let opts = match grid[y][x] {
        b'-' => [Pt { x: x + 1, y }, Pt { x: x - 1, y }],
        b'|' => [Pt { x, y: y + 1 }, Pt { x, y: y - 1 }],
        b'L' => [Pt { x: x + 1, y }, Pt { x, y: y - 1 }],
        b'J' => [Pt { x, y: y - 1 }, Pt { x: x - 1, y }],
        b'7' => [Pt { x, y: y + 1 }, Pt { x: x - 1, y }],
        b'F' => [Pt { x: x + 1, y }, Pt { x, y: y + 1 }],
        b'S' => {
            if x.checked_add(1).is_some() && [b'-', b'7', b'J'].contains(&grid[y][x + 1]) {
                return Pt { x: x + 1, y };
            }
            if y.checked_add(1).is_some() && [b'|', b'L', b'J'].contains(&grid[y + 1][x]) {
                return Pt { x, y: y + 1 };
            }
            if y.checked_sub(1).is_some() && [b'|', b'F', b'7'].contains(&grid[y - 1][x]) {
                return Pt { x, y: y - 1 };
            }
            if x.checked_sub(1).is_some() && [b'-', b'F', b'L'].contains(&grid[y][x - 1]) {
                return Pt { x: x - 1, y };
            }
            panic!("Oh no!")
        }
        _ => panic!("Should not happen"),
    };
    opts.into_iter().filter(|&pos| pos != prev).next().unwrap()
}

// fn gold(loc: &str) -> u64 {
//     let grid = read(loc);

//     let start = find_start(&grid);
//     let mut prev = start;
//     let mut now = get_next(&grid, prev, prev);
//     let mut quarter_turns = 0;

//     let mut color = vec![vec![false; grid[0].len()]; grid.len()];

//     color[start.y][start.x] = true;

//     while now != start {
//         if [b'7', b'F', b'L', b'J'].contains(&grid[now.y][now.x]) {
//             quarter_turns += match grid[now.y][now.x] {
//                 b'7' => { if now.x == prev.x + 1 { 1 } else { -1 } }
//                 b'F' => { if now.y + 1 == prev.y { 1 } else { -1 } }
//                 b'L' => { if now.x + 1 == prev.x { 1 } else { -1 } }
//                 b'J' => { if now.y == prev.y + 1 { 1 } else { -1 } }
//                 _ => panic!("Oh no!"),
//             }
//         }
//         color[now.y][now.x] = true;
//         let next = get_next(&grid, prev, now);
//         prev = now;
//         now = next;
//     }

//     println!("{quarter_turns}");
//     prnt(&grid, &color);

//     1
// }

fn gold(loc: &str) -> isize {
    let grid = read(loc);

    let start = find_start(&grid);
    let mut prev = start;
    let mut now = get_next(&grid, prev, prev);
    let mut last_corner = start;
    let mut total_area = 0;
    // let mut total_area = (last_corner.x * now.y) as isize - (now.x * last_corner.y) as isize;
    let mut total_steps = 1;
    while now != start {
        total_steps += 1;
        // color[now.y][now.x] = true;
        let next = get_next(&grid, prev, now);
        prev = now;
        now = next;
        if [b'7', b'F', b'L', b'J', b'S'].contains(&grid[now.y][now.x]) {
            total_area += (last_corner.x * now.y) as isize - (now.x * last_corner.y) as isize;
            last_corner = now;
        }
    }

    total_area = (total_area / 2).abs();

    println!("{total_area}");
    println!("{total_steps}");
    // prnt(&grid, &color);

    1 + total_area - (total_steps ) / 2
}

fn prnt_pair(grid: &Vec<Vec<u8>>, now: Pt, prev: Pt) {
    for (y, row) in grid.iter().enumerate() {
        for (x, &val) in row.iter().enumerate() {
            if now.x == x && now.y == y {
                print!("\x1b[93m{}\x1b[0m", val as char);
            } else if prev.x == x && prev.y == y {
                print!("\x1b[93m{}\x1b[0m", val as char);
            } else {
                print!("{}", val as char)
            }
        }
        println!();
    }
    println!()
}

fn prnt(grid: &Vec<Vec<u8>>, color: &Vec<Vec<bool>>) {
    for (y, row) in grid.iter().enumerate() {
        for (x, &val) in row.iter().enumerate() {
            if color[y][x] {
                print!("\x1b[93m{}\x1b[0m", val as char);
            } else {
                print!("{}", val as char)
            }
        }
        println!();
    }
    println!()
}
