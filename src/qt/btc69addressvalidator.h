// Copyright (c) 2011-2014 The Bitcoin Core developers
// Copyright (c) 2017-2019 The Raven Core developers
// Copyright (c) 2020-2021 The BTC69 Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef BTC69_QT_BTC69ADDRESSVALIDATOR_H
#define BTC69_QT_BTC69ADDRESSVALIDATOR_H

#include <QValidator>

/** Base58 entry widget validator, checks for valid characters and
 * removes some whitespace.
 */
class Bitcoin69AddressEntryValidator : public QValidator
{
    Q_OBJECT

public:
    explicit Bitcoin69AddressEntryValidator(QObject *parent);

    State validate(QString &input, int &pos) const;
};

/** btc69 address widget validator, checks for a valid btc69 address.
 */
class Bitcoin69AddressCheckValidator : public QValidator
{
    Q_OBJECT

public:
    explicit Bitcoin69AddressCheckValidator(QObject *parent);

    State validate(QString &input, int &pos) const;
};

#endif // BTC69_QT_BTC69ADDRESSVALIDATOR_H
