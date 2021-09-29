use serde_json::{self, json, Value};

use std::fs::{read_to_string, OpenOptions};
use std::io::{stdin, Read, Write};
use std::net::{TcpListener, TcpStream};
use std::process::exit;

fn get_ip() -> String {
    let mut ip = String::new();
    println!("Enter ip and port:");
    stdin().read_line(&mut ip).unwrap();
    ip = ip.trim().to_string();
    ip
}

fn main() {
    let mut users: Vec<TcpStream> = Vec::new();
    let ip = get_ip();
    let ip_for_print = ip.clone();
    let listener = match TcpListener::bind(ip) {
        Ok(k) => k,
        Err(_e) => {
            println!("wrong ip");
            exit(1);
        }
    };
    let mut users_must: usize = 0;
    println!("Server started with {}", ip_for_print);

    for stream in listener.incoming() {
        let mut stream = stream.unwrap();
        users_must = if users_must == 0 {
            let mut buffer = [0; 1024];
            let n = stream.read(&mut buffer).unwrap();
            let mes = std::str::from_utf8(&buffer[..n]).unwrap();
            println!("{}", mes);
            if mes.trim() == "save" {
                let mut buffer_login_password = [0; 1024];
                let n1 = stream.read(&mut buffer_login_password).unwrap();
                let mes_lp = std::str::from_utf8(&buffer_login_password[..n1]).unwrap();

                let mut buffer_obj = [0; 1024];
                let n2 = stream.read(&mut buffer_obj).unwrap();
                let mes_opj = std::str::from_utf8(&buffer_obj[..n2]).unwrap();

                let text = read_to_string("data.json").unwrap();
                let mut json_obj: Value = serde_json::from_str(&text).unwrap();
                let mes_s: Value = serde_json::from_str(mes_opj.clone()).unwrap();
                json_obj[mes_lp] = serde_json::from_str(&mes_opj).unwrap();

                let i: i64 = match &mes_s["coins"] {
                    Value::String(s) => s.parse().unwrap(),
                    _ => {
                        continue;
                    }
                };
                let mut min_value_index = i;
                for min in 0..json_obj["top"].as_array().unwrap().len() {
                    if min_value_index < (min as i64) {
                    } else {
                        min_value_index = min as i64;
                    }
                }
                for index in 0..json_obj["top"].as_array().unwrap().len() {
                    if json_obj["top"][index][1].as_i64().unwrap() == min_value_index {
                        json_obj["top"][index][1] = i.into();
                        json_obj["top"][index][0] = mes_s["name"].clone();
                        break;
                    }
                }
                let mut m = OpenOptions::new()
                    .write(true)
                    .truncate(true)
                    .open("data.json")
                    .unwrap();

                m.write_all(json_obj.to_string().as_bytes()).unwrap();
                m.flush();
                continue;
            }
            if mes.trim() == "top" {
                let read_file = read_to_string("data.json").unwrap();
                let json: serde_json::Value = serde_json::from_str(&read_file).unwrap();
                let js: Value = json!({"top": json["top"]});
                stream.write_all(&js.to_string().as_bytes()).unwrap();
                stream.flush().unwrap();
                continue;
            }
            if mes.trim() == "get_data" {
                let mut buffer_login_password = [0; 1024];
                let n1 = stream.read(&mut buffer_login_password).unwrap();
                let mes_lp = std::str::from_utf8(&buffer_login_password[..n1]).unwrap();

                let read_file = read_to_string("data.json").unwrap();
                let json: serde_json::Value = serde_json::from_str(&read_file).unwrap();
                //let mes_for_client = String::new();

                let mes = json[mes_lp].to_string();
                if mes == Value::Null {
                    stream.write_all("puk".as_bytes());
                } else {
                    stream.write_all(mes.as_bytes());
                }

                continue;
            }
            let mes: usize = mes.trim().parse().unwrap();

            mes
        } else {
            users_must
        };

        println!("connected {}", stream.peer_addr().unwrap());
        users.push(stream);

        if users.len() == users_must {
            println!("connect");
            let mut play = true;
            println!("game started with {} players", users_must);
            for mut user in users.iter() {
                match user.write_all("connect...Ok".as_bytes()) {
                    Ok(_) => (),
                    Err(_) => {
                        users_must = 0;
                        play = false;
                        for mut us in users.iter() {
                            us.write_all("0".as_bytes());
                            us.flush();
                        }
                    }
                };

                user.flush();
            }

            loop {
                if !play {
                    users.clear();
                    users_must = 0;
                    break;
                }
                //let mut jsons_from_users: Vec<String> = Vec::new();
                // let mut buffer = [0; 1024];
                let mut json_str_all = String::new();
                json_str_all.push('[');
                for i in 0..users.len() {
                    let mut buffer = [0; 1024];

                    let n = match users[i].read(&mut buffer) {
                        Ok(t) => t,
                        Err(_e) => {
                            println!("users disconnected");
                            for user_index in 0..users.len() {
                                if users[user_index].peer_addr().unwrap()
                                    != users[i].peer_addr().unwrap()
                                {
                                    users[user_index].write_all("0".as_bytes());
                                    users[user_index].flush();
                                }
                            }
                            users.clear();
                            play = false;
                            break;
                        }
                    };

                    let mes = std::str::from_utf8(&buffer[..n]).unwrap().trim();
                    if mes == "exit" {
                        play = false;
                        for user_index in 0..users.len() {
                            if users[user_index].peer_addr().unwrap()
                                != users[i].peer_addr().unwrap()
                            {
                                users[user_index].write_all("0".as_bytes());
                                users[user_index].flush();
                            }
                        }
                        println!("users disconnected");
                        users.clear();
                        break;
                    }
                    json_str_all.push_str(mes);
                    if i != users.len() - 1 {
                        json_str_all.push_str(", ")
                    }
                }
                json_str_all.push(']');
                if !play {
                    users_must = 0;
                    break;
                }

                for i in 0..users.len() {
                    match users[i].write_all(json_str_all.as_bytes()) {
                        Ok(_t) => (),
                        Err(_e) => {
                            println!("users disconnected");
                            for user_index in 0..users.len() {
                                if users[user_index].peer_addr().unwrap()
                                    != users[i].peer_addr().unwrap()
                                {
                                    users[user_index].write_all("0".as_bytes());
                                    users[user_index].flush();
                                }
                            }
                            users.clear();
                            play = false;
                            break;
                        }
                    }
                    users[i].flush().unwrap();
                }
                if !play {
                    break;
                }
            }
        }
    }
}
