import { Component } from '@angular/core';
import { InvestmentService } from 'src/app/services/investment.service';

@Component({
  selector: 'app-investment-calculator',
  templateUrl: './investment-calculator.component.html',
  styleUrls: ['./investment-calculator.component.css']
})
export class InvestmentCalculatorComponent {
  investmentAmount!: number;
  annualInterestRate!: number;
  years!: number;
  investmentResult: any;
  username!: string;

  constructor(private investmentService: InvestmentService) {}

  calculateInvestment() {
    // Implement the calculation logic
    this.investmentService
      .calculateInvestment(this.investmentAmount, this.annualInterestRate, this.years, this.username)
      .subscribe((result) => {
        this.investmentResult = result;
      });
  }
}
