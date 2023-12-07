use std::cmp::Ordering;
use std::collections::HashMap;
use std::mem::discriminant;

fn main() {
    println!("Hello, world!");

    println!("SILVER: The example result is : {}", silver("example.txt"));
    println!("SILVER: The result is : {}", silver("input.txt"));
    println!("GOLD: The example result is : {}", gold("example.txt"));
    println!("GOLD: The result is : {}", gold("input.txt"));
}

#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Debug)]
enum Label {
    _2,
    _3,
    _4,
    _5,
    _6,
    _7,
    _8,
    _9,
    T,
    J,
    Q,
    K,
    A,
}

impl Label {
    fn is_j(&self) -> bool {
        match self {
            Label::J => true,
            _ => false,
        }
    }
}

impl From<char> for Label {
    fn from(value: char) -> Self {
        match value {
            '2' => Label::_2,
            '3' => Label::_3,
            '4' => Label::_4,
            '5' => Label::_5,
            '6' => Label::_6,
            '7' => Label::_7,
            '8' => Label::_8,
            '9' => Label::_9,
            'T' => Label::T,
            'J' => Label::J,
            'Q' => Label::Q,
            'K' => Label::K,
            'A' => Label::A,
            _ => panic!("oh no"),
        }
    }
}

#[derive(Ord, Eq, Debug)]
struct Hand {
    cards: [Label; 5],
    bid: u64,
}

#[derive(PartialEq, Eq, PartialOrd)]
enum Type {
    HighCard,
    OnePair,
    TwoPair,
    Three,
    FullHouse,
    Four,
    Five,
}

impl Hand {
    fn get_type(&self) -> Type {
        let mut counter: HashMap<std::mem::Discriminant<Label>, i32> = HashMap::new();
        for card in self.cards {
            let d = discriminant(&card);
            counter.insert(d, 1 + *counter.get(&d).unwrap_or(&0));
        }
        match counter.len() {
            1 => Type::Five,
            2 if *counter.values().max().unwrap() == 4 => Type::Four,
            2 => Type::FullHouse,
            3 if *counter.values().max().unwrap() == 3 => Type::Three,
            3 => Type::TwoPair,
            4 => Type::OnePair,
            5 => Type::HighCard,
            _ => panic!("Oh no!"),
        }
    }

    fn get_joker_type(&self) -> Type {
        let mut counter = HashMap::new();
        for card in self.cards.iter().filter(|card| !card.is_j()) {
            let d = discriminant(card);
            counter.insert(d, 1 + *counter.get(&d).unwrap_or(&0));
        }
        let num_j = 5 - counter.values().sum::<isize>();
        match (counter.len(), num_j) {
            (_, 0) => self.get_type(),
            (2, 3) => Type::Four,
            (_, 3 | 4 | 5) => Type::Five,
            (1, _) => Type::Five,
            (2, 2) => Type::Four,
            (3, 2) => Type::Three,
            (4, 1) => Type::OnePair,
            (3, 1) => Type::Three,
            (2, 1) if *counter.values().max().unwrap() == 3 => Type::Four,
            (2, 1) => Type::FullHouse,
            _ => todo!(),
        }
    }

    fn joker_cmp(&self, other: &Self) -> std::cmp::Ordering {
        match self
            .get_joker_type()
            .partial_cmp(&other.get_joker_type())
            .unwrap()
        {
            std::cmp::Ordering::Equal => {
                for (a, b) in self.cards.iter().zip(other.cards.iter()) {
                    return match (a.is_j(), b.is_j()) {
                        (true, true) => continue,
                        (true, false) => Ordering::Less, // TODO
                        (false, true) => Ordering::Greater,
                        (false, false) if a == b => continue,
                        (false, false) => a.cmp(b),
                    };
                }
                panic!("Oh this really should not happen")
            }
            val => val,
        }
    }
}

impl PartialEq for Hand {
    fn eq(&self, other: &Self) -> bool {
        self.cards == other.cards
    }
}

impl PartialOrd for Hand {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        match self.get_type().partial_cmp(&other.get_type()).unwrap() {
            std::cmp::Ordering::Equal => self.cards.partial_cmp(&other.cards),
            val => Some(val),
        }
    }
}

fn read(loc: &str) -> Vec<Hand> {
    std::fs::read_to_string(loc)
        .unwrap()
        .lines()
        .map(|line| line.split_once(' ').unwrap())
        .map(|(cards, bid)| Hand {
            cards: cards
                .chars()
                .map(|c| Into::<Label>::into(c))
                .collect::<Vec<_>>()
                .try_into()
                .unwrap(),
            bid: bid.parse().unwrap(),
        })
        .collect()
}

fn silver(loc: &str) -> u64 {
    let mut hands = read(loc);
    hands.sort_unstable();
    hands
        .into_iter()
        .map(|hand| hand.bid)
        .enumerate()
        .map(|(rank, bid)| (1 + rank) as u64 * bid)
        .sum()
}

fn gold(loc: &str) -> u64 {
    let mut hands = read(loc);
    hands.sort_unstable_by(|s, other| {
        match s
            .get_joker_type()
            .partial_cmp(&other.get_joker_type())
            .unwrap()
        {
            std::cmp::Ordering::Equal => s.joker_cmp(other),
            val => val,
        }
    });
    hands
        .into_iter()
        .map(|hand| hand.bid)
        .enumerate()
        .map(|(rank, bid)| (1 + rank) as u64 * bid)
        .sum()
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn gold_ex() {
        assert_eq!(gold("example.txt"), 5905);
        let res = gold("input.txt");
        assert!(249577022 < res);
        assert!(249724623 < res);
    }

    #[test]
    fn order_joker() {
        use Label::*;
        let a = Hand {
            cards: [A, A, A, A, A],
            bid: 0,
        };
        let b = Hand {
            cards: [J, A, A, A, A],
            bid: 0,
        };

        let ord = a.joker_cmp(&b);
        assert!(matches!(ord, Ordering::Greater));
    }
}
