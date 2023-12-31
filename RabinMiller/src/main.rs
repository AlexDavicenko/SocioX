use std::ops::{ShlAssign, ShrAssign};
use std::time::{Instant};
use std::io;
use std::fs::File;
use std::io::Write;
use rayon::prelude::*;
use rand::prelude::*;
use num_bigint::{BigUint, RandBigInt};
use num_traits::{One, Zero};

fn main() -> io::Result<()>{
    let mut sum = 0.0;


    println!("Enter number of primes required:");
    let mut number_of_ns = String::new();
    io::stdin().read_line(&mut number_of_ns).expect("Input invalid");
    let iter: i32 = number_of_ns.trim().parse().expect("Input valid integer");

    println!("Enter number of bits:");
    let mut number_of_bits = String::new();
    io::stdin().read_line(&mut number_of_bits).expect("Input invalid");
    let bits: usize = number_of_bits.trim().parse().expect("Input valid integer");


    println!("Parallel compute? (y/n):");
    let mut parallel = String::new();
    io::stdin().read_line(&mut parallel).expect("Input invalid");
    parallel = parallel.trim().to_string();


    let mut cores: i32 = 1;

    if parallel == "y"{
        println!("Enter number of cores:");
        let mut number_of_cores = String::new();
        io::stdin().read_line(&mut number_of_cores).expect("Input invalid");
        cores = number_of_cores.trim().parse().expect("Input valid integer");
    }

    println!("Enter filename to write to:");
    let mut filename = String::new();
    io::stdin().read_line(&mut filename).expect("Input valid string");
    filename = filename.trim().to_string();

    let mut file = File::create(filename)?;
    for i in 0 ..iter{

        println!("\nFinding {bits} bit primes");

        let start_time = Instant::now();
        let ans = if parallel == "y" {find_prime_parallel(bits, cores as usize)} else { find_prime(bits) };
        let end_time = Instant::now();

        println!("Finished in {:?}", end_time.duration_since(start_time));
        sum += end_time.duration_since(start_time).as_secs_f64();
        println!("{ans}");
        file.write((ans.to_string()+"\n").as_ref()).expect("Failed writing to file");
        
    }

    print!("Average time taken: {}", sum/(iter as f64));
    Ok(())
}


fn rm_test(n: &BigUint, a: &BigUint) -> bool{


    let mut exp = n - BigUint::one();
    let n_minus_1 = n - BigUint::one();


    //While the last bit is zero (exp is even)
    while !exp.bit(0){
        exp.shr_assign(1)
    }

    if a.modpow(&exp, n) == BigUint::one(){
        return true;
    }
    while exp < n_minus_1 {

        if a.modpow(&exp, n) == n_minus_1{
            return true;
        }
        exp.shl_assign(1);
    }


    return false;


}

fn rabin_miller_parallel(n: &BigUint, k: usize) -> bool{


    let result_array: Vec<bool> = vec![true; k];

    let found = result_array.par_iter().find_any(|_|{
        let a = random_bint_in_range(BigUint::one() << 1, n-(BigUint::one() << 1));

        if rm_test(n, &a) == false{
            return true;
        }
        return false;
    });

    return match found {
        Some(_) => false,
        None => true,
    }

}

fn rabin_miller(n: &BigUint, k: i32) -> bool{

    for _ in 0..k{
        //Choose random a between 1 < a < n-1

        let a = random_bint_in_range(BigUint::one() << 1, n-(BigUint::one() << 1));

        if rm_test(n, &a) == false{
            return false;
        }


    }
    return true;
}
fn random_bint_in_range(min: BigUint, max: BigUint) -> BigUint{
    //Inclusive of both min and max
    let mut rng = thread_rng();

    let range = max.clone() - min.clone() + BigUint::one();
    let random_offset = rng.gen_biguint(max.bits()) % range;
    return &min + random_offset;
}
fn find_prime(bits: usize) -> BigUint{

    //let n = BigUint::one() << bits;

    let mut counter = 0;
    loop {

        let n = (random_bint_in_range(
            BigUint::one() << (bits-1),
            BigUint::one() << bits) << 1)  + BigUint::one();

        //println!("Testing {n}");
        counter += 1;
        println!("Numbers checked {counter}");

        if rabin_miller(&n, 50){
            println!("Numbers checked {counter}");
            return n;
        }

    }
}

fn find_prime_parallel(bits: usize, cores: usize) -> BigUint{



    let mut counter = 0;
    loop {
        let mut primes_array: Vec<BigUint> = vec![BigUint::zero(); cores];

        primes_array.par_iter_mut().for_each(|n|{


            let x = (random_bint_in_range(
                BigUint::one() << (bits-2),
                (BigUint::one() << (bits-1)) - BigUint::one()) << 1)  + BigUint::one();

            if rabin_miller(&x, 50){
                *n = x.clone();
            }
        });
        counter += cores;
        println!("Numbers checked {counter}");


        for big_int in primes_array{
            if big_int != BigUint::zero(){
                println!("Numbers checked {counter}");
                return big_int;
            }
        }

    }


}