//! Generate the CheckCodePrefix enum.

use std::collections::{BTreeMap, BTreeSet};

use codegen::{Scope, Type, Variant};
use itertools::Itertools;
use ruff::checks::CheckCode;
use strum::IntoEnumIterator;

fn main() {
    // Build up a map from prefix to matching CheckCodes.
    let mut prefix_to_codes: BTreeMap<String, BTreeSet<CheckCode>> = Default::default();
    for check_code in CheckCode::iter() {
        let as_ref = check_code.as_ref().to_string();
        for i in 1..=as_ref.len() {
            let prefix = as_ref[..i].to_string();
            let entry = prefix_to_codes
                .entry(prefix)
                .or_insert_with(|| Default::default());
            entry.insert(check_code.clone());
        }
    }

    let mut scope = Scope::new();

    // Create the `CheckCodePrefix` definition.
    let mut gen = scope
        .new_enum("CheckCodePrefix")
        .vis("pub")
        .derive("EnumString")
        .derive("Debug")
        .derive("PartialEq")
        .derive("Eq")
        .derive("Clone")
        .derive("Serialize")
        .derive("Deserialize");
    for (prefix, _) in &prefix_to_codes {
        gen = gen.push_variant(Variant::new(prefix.to_string()));
    }

    // Create the `PrefixSpecificity` definition.
    scope
        .new_enum("PrefixSpecificity")
        .vis("pub")
        .derive("PartialEq")
        .derive("Eq")
        .derive("PartialOrd")
        .derive("Ord")
        .push_variant(Variant::new("Category"))
        .push_variant(Variant::new("Hundreds"))
        .push_variant(Variant::new("Tens"))
        .push_variant(Variant::new("Explicit"));

    // Create the `match` statement, to map from definition to relevant codes.
    let mut gen = scope
        .new_impl("CheckCodePrefix")
        .new_fn("codes")
        .arg_ref_self()
        .ret(Type::new("Vec<CheckCode>"))
        .vis("pub")
        .line("match self {");
    for (prefix, codes) in &prefix_to_codes {
        gen = gen.line(format!(
            "CheckCodePrefix::{prefix} => vec![{}],",
            codes
                .iter()
                .map(|code| format!("CheckCode::{}", code.as_ref()))
                .join(", ")
        ));
    }
    gen.line("}");

    // Create the `match` statement, to map from definition to specificity.
    let mut gen = scope
        .new_impl("CheckCodePrefix")
        .new_fn("specificity")
        .arg_ref_self()
        .ret(Type::new("PrefixSpecificity"))
        .vis("pub")
        .line("match self {");
    for (prefix, _) in &prefix_to_codes {
        let specificity = match prefix.len() {
            4 => "Explicit",
            3 => "Tens",
            2 => "Hundreds",
            1 => "Category",
            _ => panic!("Invalid prefix: {}", prefix),
        };
        gen = gen.line(format!(
            "CheckCodePrefix::{prefix} => PrefixSpecificity::{},",
            specificity
        ));
    }
    gen.line("}");

    println!("//! File automatically generated by examples/generate_check_code_prefix.rs.");
    println!();
    println!("use serde::{{Serialize, Deserialize}};");
    println!("use strum_macros::EnumString;");
    println!();
    println!("use crate::checks::CheckCode;");
    println!();
    println!("{}", scope.to_string());
}
